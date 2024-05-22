import wx

import includes
import main
import fetcher
import commclasses as CC

class InitialSetup(wx.Frame):
    def __init__(self, *args, **kw):
        super(InitialSetup, self).__init__(*args, **kw)

        pnl = wx.Panel(self)


        st = wx.StaticText(pnl, label="Initial Game chooser")
        font = st.GetFont()
        font.PointSize += 10
        font = font.Bold()
        st.SetFont(font)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(st, wx.SizerFlags().Border(wx.TOP|wx.LEFT, 25))
        pnl.SetSizer(sizer)

        self.makeMenuBar()

        self.CreateStatusBar()
        self.SetStatusText(includes.AppName + " " + includes.Version)

        #self.FetchWindow(self)

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