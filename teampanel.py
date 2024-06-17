import wx

import wx
import includes
import commclasses as CC
import scoreboard as SB



class PlayerInfoPanel(wx.Panel):

    def __init__(self, parent, title, player):
        super().__init__(parent)
        numFont = wx.Font(wx.FontInfo(40).Bold())
        self.PNumber = wx.StaticText(self, -1,  str(69), size=(250,250))
        self.PNumber.SetFont(numFont)
        SNameFont = wx.Font(wx.FontInfo(30).Bold())
        self.PSName = wx.StaticText(self, -1,"WANKER")
        self.PSName.SetFont(SNameFont)
        # PFNAME = wx.StaticText(self, -1, "Hezar")
        # PPGuide = wx.StaticText(self, -1,"He's a wanker")
        # PGameGoals = wx.StaticText(self, -1, str(0))
        # PGameAssists = wx.StaticText(self, -1, str(0))
        # PGamePIM = wx.StaticText(self, -1, str(4))

        box = wx.StaticBox(self, -1, "Player staticbox")
        bsizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)
        #player.GameNumber = 99
        t = wx.StaticText(self, -1, title)
        bsizer.Add(self.PNumber, 1, wx.LEFT)
        bsizer.Add(self.PSName,0,wx.TOP|wx.RIGHT, 10)


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
        panel=PlayerInfoPanel(self,player="foo", title="bar")
        #panel=TeamPanel(self, )
        self.Show()
