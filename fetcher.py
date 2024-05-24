import time

import includes
import urllib.request, json
import wx
import time
import xml.etree.ElementTree as ET
import commclasses as CC
import scoreboard as SB

def getGameDataURL(game_id):
    # build the query string
    QueryURL = includes.API_URL_Base + "games/game?game_id=" + str(game_id) + "&xsyte_id=" + str(includes.xsyte_id) + "&format=json"

    return(QueryURL)


def getGameData(game_id):
    jsonURL = getGameDataURL(game_id=game_id)
    print(jsonURL)
    gameDataJSON =  urllib.request.urlopen(jsonURL).read()
    gameData = json.loads(gameDataJSON)
    gameData["fetchedAt"] = wx.DateTime.Now()
    return(gameData)


# pulse - we'll pull the data from xcyte every JSONRefreshInterval using wx.timer()

class FetchWindow(wx.Window):
    def __init__(self, parent):
        wx.Window.__init__(self,parent)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)
        self.timer.Start(1000)

    def Draw(selfself,dc):
        t = time.localtime(time.time())
        st = time.strftime("%I:%M:%S", t)
        w,h = self.GetClientSize()
        dc.SetBackground(wx.Brush(self.GetBackgoundColour()))
        dc.Clear()
        dc.SetFont(wx.Font(30, wx.SWISS_FONT, wx.NORMAL_FONT, wx.NORMAL_FONT))
        tw, th = dc.GetTextExtent(st)
        dc.DrawText(st, (w-tw)/2, (h)/2 - th/2)

    def OnTimer(self, evt):
        dc = wx.AutoBufferedPaintDC(wx.ClientDC(self))
        self.Draw(dc)

