import wx
import wx.gizmos as gizmos

import includes
import main
import fetcher
import commclasses as CC
import game_setup
import dummydata as DD
import scoreboard as SB

# global to this module, urk...
SBD = SB.ScoreBoard()
ThisGame = CC.Game(GameID=includes.defaultGameID)
xciteGameDataSnapshot = fetcher.getGameData(game_id=includes.gameID)


class InitialSetup(wx.Frame):
    def __init__(self, *args, **kw):
        super(InitialSetup, self).__init__(*args, **kw)

        panel = wx.Panel(self)


        st = wx.StaticText(panel, label="Scoreboard Mirror")
        font = st.GetFont()
        font.PointSize += 10
        font = font.Bold()
        st.SetFont(font)

        # the game clock
        self.PClock = wx.StaticText(panel, label="00:00", style=wx.ALIGN_CENTER)
        font = self.PClock.GetFont()
        font.PointSize += 10
        font = font.Bold()

        self.PClock.SetFont(font)
        self.PClock.SetForegroundColour((0,0,0))


        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(st, wx.SizerFlags().Border(wx.TOP|wx.LEFT, 25))
        panel.SetSizer(sizer)

        #size = wx.DefaultSize
        #style = gizmos.LED_ALIGN_CENTER
        #pos = wx.DefaultPosition
        #self.led = gizmos.LEDNumberCtrl(self, -1, pos, size, style)
        # default colours are green on black
        #self.led.SetBackgroundColour("blue")
        #self.led.SetForegroundColour("yellow")
        #self.led.SetValue("123456789")


        # this is the refresh timer stuff, grabs data from the scoreboard and xcite API
        # this is background, the loads -may- block, does wx have threads?!
        #self.SBLoadCounter = 0
        #SBD = SB.ScoreBoard()
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
        self.SBTimer.Start(int(includes.ScoreBoardPollIntervalSeconds * 1000.0))
        self.XCITETimer.Start(includes.JSONRefreshInterval * 1000)
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
        ClockString = "%02d:%02d" % (SBD.PeriodTimeLeft.minute, SBD.PeriodTimeLeft.second)
        PeriodString = "%s" % (str(SBD.Period))
        print(ClockString)
        self.PClock.SetLabel(ClockString)
        if (SBD.PeriodStatus == True):
            self.PClock.SetForegroundColour((0, 0, 0))
            print("Period", SBD.Period, ":", SBD.PeriodTimeLeft.minute,SBD.PeriodTimeLeft.second, end=' ')
            if (SBD.PeriodTimeLeft.microsecond):
                print(SBD.PeriodTimeLeft.microsecond, end=' ; ')
        else:
            self.PClock.SetForegroundColour((255, 0, 0))
            print("Period (paused)", SBD.Period, ":", SBD.PeriodTimeLeft.minute, SBD.PeriodTimeLeft.second, end=' ')
            if (SBD.PeriodTimeLeft.microsecond):
                print(SBD.PeriodTimeLeft.microsecond, end=' ; ')
        print(SBD.HomeTeamName, ": ", SBD.HomeTeamScore, " (", SBD.HomeTeamShots,") ", SBD.AwayTeamName, ": ", SBD.AwayTeamScore, " (", SBD.AwayTeamShots, ") ", sep='')
        if SBD.HomeTeamPenalties:
            print(SBD.HomeTeamName, "Penalty : ", end='')
            for penalty in SBD.HomeTeamPenalties:
                print(penalty.Number, penalty.timeLeft, ' ', end='')
        if SBD.AwayTeamPenalties:
            print(SBD.AwayTeamName, "Penalty : ", end='')
            for penalty in SBD.AwayTeamPenalties:
                print(penalty.Number, penalty.timeLeft, ' ', end='')
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


    def OnExit(self, event):
        self.Close(True)

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
        #print(gameDataSnapshot["fetchedAt"])
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