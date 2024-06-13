import wx
import wx.gizmos as gizmos
import re

import includes
import main
import fetcher
import commclasses as CC
import game_setup
import dummydata as DD
import scoreboard as SB
import teampanel as TP

# global to this module, urk...
SBD = SB.ScoreBoard()
ThisGame = CC.Game(GameID=includes.defaultGameID)
xciteGameDataSnapshot = fetcher.getGameData(game_id=includes.gameID)
HomePlayersByNum = {}
AwayPlayersByNum = {}


class InitialSetup(wx.Frame):
    def __init__(self, *args, **kw):
        super(InitialSetup, self).__init__(*args, **kw)

        panel = wx.Panel(self)
        mainSizer = wx.BoxSizer(orient=wx.VERTICAL)


        # the game clock
        self.PClock = wx.StaticText(panel, label="00:00", style=wx.ALIGN_CENTER)
        font = self.PClock.GetFont()
        font.PointSize += 10
        font = font.Bold()

        self.PClock.SetFont(font)
        self.PClock.SetForegroundColour((0,0,0))
        self.PClock.SetBackgroundColour((250,230,230))

        # the period identifier
        self.WhatPeriodText = "no game yet"
        self.WhatPeriodBox = wx.StaticText(panel, label=self.WhatPeriodText, style=wx.ALIGN_CENTRE)
        self.WhatPeriodBox.SetFont(font)


        PeriodSizer = wx.BoxSizer()
        PeriodSizer.Add(self.WhatPeriodBox, border=5)
        PeriodSizer.Add(self.PClock, border=5)
        # PeriodSizer.Add(st)
        #panel.SetSizer(PeriodSizer)

        mainSizer.Add(PeriodSizer)
        # split the box in half, we'll have HOME : AWAY sizers as half each for the rest of the
        homeawaySizer = wx.BoxSizer(orient=wx.HORIZONTAL)
        homeSizer = wx.BoxSizer(orient=wx.VERTICAL)
        awaySizer = wx.BoxSizer(orient=wx.VERTICAL)
        homeScoreSizer = wx.BoxSizer(orient=wx.HORIZONTAL)
        awayScoreSizer = wx.BoxSizer(orient=wx.HORIZONTAL)
        homeawaySizer.Add(homeSizer, proportion = 1, flag = wx.ALL | wx.EXPAND, border = 5)
        homeawaySizer.Add(awaySizer, proportion = 1, flag = wx.ALL | wx.EXPAND, border = 5)

        self.homeTag = wx.StaticText(panel,label="HOME")
        self.homeTag.SetFont(font)
        self.homeScore = wx.StaticText(panel, label="0")
        self.homeScore.SetFont(font)
        self.homeShots = wx.StaticText(panel, label="0")
        self.homeShots.SetFont(font)

        self.awayTag = wx.StaticText(panel, label="AWAY")
        self.awayTag.SetFont(font)
        self.awayScore = wx.StaticText(panel, label="0")
        self.awayScore.SetFont(font)
        self.awayShots = wx.StaticText(panel, label="0")
        self.awayShots.SetFont(font)


        homeSizer.Add(self.homeTag)
        homeSizer.Add(homeScoreSizer)
        homeScoreSizer.Add(self.homeScore, proportion = 1, flag = wx.ALL | wx.EXPAND, border = 5)
        homeScoreSizer.Add(self.homeShots, proportion = 1, flag = wx.ALL | wx.EXPAND, border = 5)

        awaySizer.Add(self.awayTag)
        awaySizer.Add(awayScoreSizer)
        awayScoreSizer.Add(self.awayScore, proportion=1, flag=wx.ALL | wx.EXPAND, border=5)
        awayScoreSizer.Add(self.awayShots, proportion=1, flag=wx.ALL | wx.EXPAND, border=5)

        mainSizer.Add(homeawaySizer, proportion = 1, flag = wx.ALL | wx.EXPAND, border = 5)

        #penSizer = wx.BoxSizer(orient=wx.HORIZONTAL)
        homePenSizer = wx.BoxSizer(orient=wx.VERTICAL)
        awayPenSizer = wx.BoxSizer(orient=wx.VERTICAL)
        homeSizer.Add(homePenSizer, proportion = 1, flag = wx.ALL | wx.EXPAND, border = 1)
        awaySizer.Add(awayPenSizer, proportion = 1, flag = wx.ALL | wx.EXPAND, border = 2)

        self.homePenTag = wx.StaticText(panel, label = "")
        self.homePenTag.SetFont(font)
        homePenSizer.Add(self.homePenTag)

        self.awayPenTag = wx.StaticText(panel, label="")
        self.awayPenTag.SetFont(font)
        awayPenSizer.Add(self.awayPenTag)

        #mainSizer.Add(penSizer)






        panel.SetSizer(mainSizer)
        # this is the refresh timer stuff, grabs data from the scoreboard and xcite API
        # this is background, the loads -may- block, does wx have threads?!
        print(SBD.SBName, SBD.SBVersion)

        if(SBD.PeriodStatus == True):
            print("Period :", SBD.Period, SBD.PeriodTimeLeft)
        else:
            print("Period (paused) : ", SBD.Period, SBD.PeriodTimeLeft)
        print(SBD.HomeTeamName, ":", SBD.HomeTeamScore, " .... ", SBD.AwayTeamName, ":", SBD.AwayTeamScore)
        #print('Time left in period :', scoreboard.PeriodTimeLeft)

        # the event loop that fetches scoreboard and xcite data
        self.SBTimer = wx.Timer(self, 1)
        self.XCITETimer = wx.Timer(self, 2)
        self.SBTimer.Start(includes.ScoreBoardPollIntervalMicroSeconds)
        self.XCITETimer.Start(includes.JSONRefreshInterval)
        self.Bind(wx.EVT_TIMER, self.SBUpdate, id=1)
        self.Bind(wx.EVT_TIMER, self.XCiteUpdate, id=2)
        # end loop


        self.makeMenuBar()

        self.CreateStatusBar()
        self.SetStatusText(includes.AppName + " " + includes.Version)

        #self.FetchWindow(self)

    def SBUpdate(self, event):

        #print("update the scoreboard data from the XML file")
        SBD.reload()

        PeriodString = "Period : %s" % (str(SBD.Period))
        #print(ClockString)
        FullClockString = ""
        self.homeTag.Label = SBD.HomeTeamName
        self.awayTag.Label = SBD.AwayTeamName
        self.WhatPeriodBox.SetLabel(PeriodString)
        ClockString = "  %02d:%02d  " % (SBD.PeriodTimeLeft.minute, SBD.PeriodTimeLeft.second)
        print(ClockString, end= " ")
        if ((SBD.PeriodTimeLeft.minute == 0) and (SBD.PeriodTimeLeft > includes.zerotime)):
            # switch to high res with under a minute to go
            if self.SBTimer.Interval == includes.ScoreBoardPollIntervalMicroSeconds:
                self.SBTimer.Start(includes.HiResScoreBoardPollIntervalMicroSeconds)
            print(SBD.PeriodTimeLeft.microsecond, end=' ; ')
            FullClockString = "%02d.%d" % (SBD.PeriodTimeLeft.second, (SBD.PeriodTimeLeft.microsecond / 100000))
        else:
            # put the clock back to slower samples
            if self.SBTimer.Interval == includes.HiResScoreBoardPollIntervalMicroSeconds:
                self.SBTimer.Start(includes.ScoreBoardPollIntervalMicroSeconds)
            FullClockString = ClockString
        self.PClock.SetLabel(FullClockString)
        print(FullClockString)

        if (SBD.PeriodStatus == True):
            self.PClock.SetForegroundColour((0, 0, 0))
        else:
            self.PClock.SetForegroundColour((255,0,0))
        homeTeamFullScore = "%d (%d)" % (int(SBD.HomeTeamScore), int(SBD.HomeTeamShots))
        self.homeScore.Label = SBD.HomeTeamScore
        self.homeShots.Label = SBD.HomeTeamShots
        #self.homeFullScore.Label = homeTeamFullScore
        awayTeamFullScore = "%d (%d)" % (int(SBD.AwayTeamScore), int(SBD.AwayTeamShots))
        #self.awayFullScore.Label = awayTeamFullScore
        self.awayScore.Label = SBD.AwayTeamScore
        self.awayShots.Label = SBD.AwayTeamShots



        print(SBD.HomeTeamName, ": ", SBD.HomeTeamScore, " (", SBD.HomeTeamShots,") ", SBD.AwayTeamName, ": ", SBD.AwayTeamScore, " (", SBD.AwayTeamShots, ") ", sep='')
        if SBD.HomeTeamPenalties:
            homePenString = ""
            print(SBD.HomeTeamName, "Penalty : ", end='')
            for penalty in SBD.HomeTeamPenalties:
                criminal = ""
                if penalty.Number in HomePlayersByNum:
                    criminal = " " + HomePlayersByNum[penalty.Number].SirName
                print(penalty.Number, penalty.timeLeft, ' ', end='')
                homePenString += str(penalty.Number) + criminal + " : " + penalty.timeLeft + "\n"
            self.homePenTag.Label = homePenString
        else:
            self.homePenTag.Label = ""
        if SBD.AwayTeamPenalties:
            awayPenString = ""
            print(SBD.AwayTeamName, "Penalty : ", end='')
            for penalty in SBD.AwayTeamPenalties:
                criminal = ""
                if penalty.Number in AwayPlayersByNum:
                    criminal = " " + HomePlayersByNum[penalty.Number].SirName
                print(penalty.Number, penalty.timeLeft, ' ', end='')
                awayPenString += str(penalty.Number) + criminal + " : " + penalty.timeLeft + "\n"
            self.awayPenTag.Label = awayPenString
        else:
            self.awayPenTag.Label = ""
        if (SBD.HomeTeamPenalties or SBD.AwayTeamPenalties):
            print()

    def XCiteUpdate(self, event):
        print("updating the XCITE and database info")
        #     gameData["fetchedAt"] = wx.DateTime.Now()
        print(ThisGame)


    def makeMenuBar(self):
        fileMenu = wx.Menu()
        helloItem = fileMenu.Append(-1,"&Hello...\tCtrl-H", "Help string shown in status")
        fileMenu.AppendSeparator()

        exitItem = fileMenu.Append(wx.ID_EXIT)

        gameMenu = wx.Menu()
        gameChooserItem = gameMenu.Append(-1,"&Game", "Choose a game by xcite game ID")
        gameRefreshIntervalItem = gameMenu.Append(-1, "&Refresh Interval", "delay between polling the xCite API in seconds")
        gameSBReadRestartItem = gameMenu.Append(-1, "Restart SB reading")


        helpMenu = wx.Menu()
        aboutItem = helpMenu.Append(wx.ID_ABOUT)

        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "&File")
        menuBar.Append(gameMenu, "&Game")
        menuBar.Append(helpMenu, "&Help")


        self.SetMenuBar(menuBar)

        self.Bind(wx.EVT_MENU, self.OnExit, exitItem)

        self.Bind(wx.EVT_MENU, self.OnGameChooser, gameChooserItem)
        self.Bind(wx.EVT_MENU, self.OnGameRefreshIntervalChooser, gameRefreshIntervalItem)
        self.Bind(wx.EVT_MENU, self.OnGameSBReadRestartChooser, gameSBReadRestartItem)


    def OnExit(self, event):
        self.Close(True)

    def OnGameSBReadRestartChooser(self, event):
        includes.OkToReadSBFile = True

    def OnGameChooser(self, event):
        print("choose a game")
        prompt = "Select Game ID (from Hockeysyte) (", includes.gameID, ")"
        print(prompt)
        newVal = wx.NumberEntryDialog(self, message = "Game ID is from HockeySyte", prompt = str(prompt), caption = "Game Chooser", value=includes.gameID, min = 1, max = 100000)
        if newVal.ShowModal() == wx.ID_OK:
            newVal.Show()
            print(" new game ID : ", newVal.GetValue())
        includes.gameID = newVal.GetValue()
        CC.Game.xciteGameID = includes.gameID
        newVal.Destroy()
        gameDataSnapshot = fetcher.getGameData(game_id=includes.gameID)
        # print(gameDataSnapshot["teams"][0]["team_full_name"], "vs", gameDataSnapshot["teams"][1]["team_full_name"])
        # teams = gameDataSnapshot["teams"][0]["team_full_name"] + " vs " + gameDataSnapshot["teams"][1]["team_full_name"]
        CC.HomeTeam.Name = gameDataSnapshot["teams"][0]["team_full_name"]
        CC.AwayTeam.Name = gameDataSnapshot["teams"][1]["team_full_name"]
        HomePlayersFromHS = gameDataSnapshot['teams'][0]['roster']
        AwayPlayersFromHS = gameDataSnapshot['teams'][1]['roster']
        for HomePlayerFromHS in HomePlayersFromHS:
            # print(HomePlayerFromHS)
            player = CC.Player(FirstName=HomePlayerFromHS['firstname'], SirName=HomePlayerFromHS['lastname'],
                               xcitePlayerID=int(HomePlayerFromHS['player_id']),
                               GameNumber=self.fixPlayerNumber(HomePlayerFromHS['jersey_number']))

            # print('injecting : ", player.FirstName, player.)
            HomePlayersByNum[player.GameNumber] = player
            #exit()
        for playerNum in HomePlayersByNum:
            print(HomePlayersByNum[playerNum].FirstName, HomePlayersByNum[playerNum].SirName, HomePlayersByNum[playerNum].GameNumber)
        for AwayPlayerFromHS in AwayPlayersFromHS:
            player = CC.Player(FirstName=AwayPlayerFromHS['firstname'], SirName=AwayPlayerFromHS['lastname'],
                               xcitePlayerID=int(AwayPlayerFromHS['player_id']),
                               GameNumber=self.fixPlayerNumber(AwayPlayerFromHS['jersey_number']))
            AwayPlayersByNum[player.GameNumber] = player
        for playerNum in AwayPlayersByNum:
            print(AwayPlayersByNum[playerNum].FirstName, AwayPlayersByNum[playerNum].SirName, AwayPlayersByNum[playerNum].GameNumber)
        # print(HomePlayersByNum)
        # print(gameDataSnapshot["fetchedAt"])
        # print(str(teams))
        print("Home : ", CC.HomeTeam.Name, "Away : ", CC.AwayTeam.Name)
        print("Fetched at : " + str(gameDataSnapshot["fetchedAt"]))

    def OnGameRefreshIntervalChooser(self, event):
        #print(includes.JSONRefreshInterval)
        #refreshInterval
        print("set a refresh interval, currently :", includes.JSONRefreshInterval)
        prompt = "Refresh Interval (" + str(includes.JSONRefreshInterval) + ") : "
        print(prompt)
        # poo = wx.NumberEntryDialog()
        # bloot = poo.ShowModal()
        newVal = wx.NumberEntryDialog(self,message = "Time between updates from HockeySyte", prompt = str(prompt), caption = "Enter seconds", value = includes.JSONRefreshInterval, min = 1, max = 60)
        if newVal.ShowModal() == wx.ID_OK:
            newVal.Show()
            print("new interval : ", newVal.GetValue())
        includes.JSONRefreshInterval = newVal.GetValue()
        newVal.Destroy()

    def fixPlayerNumber(self, suppliedNumber):
        # player number *should* be an integer. Sometimes it's G33 (goalie, fsck() knows why ....
        # print("checking : ", suppliedNumber)
        try:
            num = int(suppliedNumber)
        except:
            # it's something funky ... probably G33 or something - if it's a "G" it's a goalie at iceHQ so we'll just strip the G
            #print("player number from hockeysyte is NAN!", suppliedNumber)
            res = [re.findall(r'(\d+)', suppliedNumber)[0] ]
            #print(res)
            num = int(res[0])
            #print("returning ", num)

        return num
