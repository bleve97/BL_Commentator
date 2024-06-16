# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# https://icehq.hockeysyte.com/api/games/game?game_id=6024&xsyte_id=347&format=json

import includes
import fetcher
#import urllib.request, json
import wx
import game_setup
import teampanel as TP
#import commclasses as CC
import dummydata as DD
#import scoreboard as SB


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #JSONrefreshInterval = includes.DefaultJSONRefreshInterval
    print("wxPython v" +  wx.VERSION_STRING)
    print('Data API URL : ', includes.API_URL_Base)

    app = wx.App()
    frm = game_setup.InitialSetup(None, title=includes.AppName)
    #thisGame = CC.Game(GameID=1)

    #print(thisGame)
    #print(DD.dummyHome.Name, DD.dummyHome.TeamID)
    frm.Show()
    frm.Size = includes.InitialFrameSize

    #HTF = TP.TeamFrame(title="Home Team", parent=wx.GetTopLevelParent(frm))
    #HTF.Size = includes.InitialTeamFrameSize
    #AWF = TP.TeamFrame(title="Away Team", parent=wx.GetTopLevelParent(frm))
    #AWF.Size = includes.InitialTeamFrameSize
    app.MainLoop()

