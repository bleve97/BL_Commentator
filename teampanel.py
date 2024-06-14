import wx

import wx
import includes
import commclasses as CC
import scoreboard as SB

class TeamFrame(wx.Frame):

    def __init__(self, title, parent=None):
        wx.Frame.__init__(self, parent=parent, title=title)
        self.Show()


class TeamPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        main_sizer = wx.BoxSizer(wx.VERTICAL)
class PlayerInfoPanel():
    def __init__(self):
        print("hi")
    # hi

