import wx

import wx
import includes
import commclasses as CC
import scoreboard as SB



class PlayerInfoPanel(wx.Panel):

    def __init__(self, parent, player):
        super().__init__(parent)
        box = wx.StaticBox(self, -1, "Player staticbox")
        bsizer = wx.StaticBoxSizer(box, wx.VERTICAL)

        t = wx.StaticText(self, -1, "hi there")
        bsizer.Add(t,0,wx.TOP|wx.LEFT, 10)

        border = wx.BoxSizer()
        border.Add(bsizer, 1, wx.EXPAND|wx.ALL, 25)
        self.SetSizer(border)





class TeamPanel(wx.Panel):

    def __init__(self, parent):
        super().__init__(parent)
        main_sizer = wx.BoxSizer(wx.VERTICAL)
#class PlayerInfoPanel():
#    def __init__(self):
#        print("hi")
    # hi


class TeamFrame(wx.Frame):

    def __init__(self, title, parent=None):
        wx.Frame.__init__(self,parent=parent, title=title)
        panel=PlayerInfoPanel(self,player="foo")
        self.Show()
