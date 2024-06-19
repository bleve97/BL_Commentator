import wx

import wx
import includes
import commclasses as CC
import scoreboard as SB



class PlayerInfoPanel(wx.Panel):

    def __init__(self, parent, title, player):
        super().__init__(parent)
        numFont = wx.Font(wx.FontInfo(40).Bold())
        self.PNumber = wx.StaticText(self, -1,  str(player.GameNumber), size=(250,250))
        self.PNumber.SetFont(numFont)
        SNameFont = wx.Font(wx.FontInfo(30).Bold())
        self.PSName = wx.StaticText(self, -1,player.SirName)
        self.PSName.SetFont(SNameFont)

        FNameFont = wx.Font(wx.FontInfo(15).Bold())
        self.PFName = wx.StaticText(self, -1, player.FirstName)
        self.PFName.SetFont(FNameFont)

        if (player.PronunciationGuide):
            self.Pronounce = wx.StaticText(self, -1, player.PronunciationGuide)
            self.Pronounce.SetFont(FNameFont)
        # PFNAME = wx.StaticText(self, -1, "Hezar")
        # PPGuide = wx.StaticText(self, -1,"He's a wanker")
        # PGameGoals = wx.StaticText(self, -1, str(0))
        # PGameAssists = wx.StaticText(self, -1, str(0))
        # PGamePIM = wx.StaticText(self, -1, str(4))

        box = wx.StaticBox(self, -1, "Player staticbox")
        bsizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)

        numBox = wx.StaticBox(self, -1, "Number")
        numBoxSizer = wx.StaticBoxSizer(numBox)
        numBoxSizer.Add(self.PNumber)

        nameBox = wx.StaticBox(self, -1, "Name")
        nameBoxSizer = wx.StaticBoxSizer(nameBox, wx.VERTICAL)
        nameBoxSizer.Add(self.PSName, 0, wx.TOP|wx.LEFT, 10)
        nameBoxSizer.Add(self.PFName, 0, wx.BOTTOM, wx.LEFT, 10)
        if (player.PronunciationGuide):
            nameBoxSizer.Add(self.Pronounce, 0, wx.BOTTOM|wx.RIGHT, 0)
        t = wx.StaticText(self, -1, title)
        # bsizer.Add(self.PNumber, 1, wx.LEFT)
        bsizer.Add(numBoxSizer, 0, wx.LEFT, 5)
        bsizer.Add(nameBoxSizer, 0, wx.RIGHT, 5)

        #bsizer.Add(self.PSName,0,wx.TOP|wx.RIGHT, 10)


        border = wx.BoxSizer()
        border.Add(bsizer, 1, wx.EXPAND|wx.ALL, 25)
        self.SetSizer(border)





class TeamPanel(wx.Panel):

    def __init__(self, parent, teamName):
        super().__init__(parent)
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        title = wx.StaticBox(self, -1, teamName)
        main_sizer.Add(title, 0, wx.TOP|wx.LEFT, 10)

        self.SetSizer(main_sizer)
#class PlayerInfoPanel():
#    def __init__(self):
#        print("hi")
    # hi


class TeamFrame(wx.Frame):

    def __init__(self, title, parent=None):
        wx.Frame.__init__(self,parent=parent, title=title)
        testPlayer = CC.Player(PlayerID = 1234, GameNumber = 69, FirstName = "Ernie", SirName = "Vanker", PronunciationGuide="WANKer")
        panel=PlayerInfoPanel(self,player=testPlayer, title="bar")
        #panel=TeamPanel(self, )
        self.Show()
