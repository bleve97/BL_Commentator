import wx

import wx
import includes
import commclasses as CC
import scoreboard as SB

class TeamFrame(wx.Frame):

    def __init__(self, title, parent=None):
        wx.Frame.__init__(self, parent=parent, title=title)
        self.Show()


class PlayerInfo():
    def __init__(self):
        print("hi")
    # hi

