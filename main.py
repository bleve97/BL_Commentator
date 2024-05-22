# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# https://icehq.hockeysyte.com/api/games/game?game_id=6024&xsyte_id=347&format=json

import includes
import fetcher
import urllib.request, json
import wx
import game_setup
import commclasses as CC
import dummydata as DD
import scoreboard as SB


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #JSONrefreshInterval = includes.DefaultJSONRefreshInterval
    print("wxPython v" +  wx.VERSION_STRING)
    print('Data API URL : ', includes.API_URL_Base)
    print('default refresh interval(s) : ', includes.JSONRefreshInterval)

    from asyncio.events import get_event_loop
    app = wx.App()
    frm = game_setup.InitialSetup(None, title=includes.AppName)
    thisGame = CC.Game(GameID=1)
    scoreboard = SB.ScoreBoard()
    print(scoreboard.SBName, scoreboard.SBVersion, scoreboard.PeriodStatus, scoreboard.HomeTeamName)
    print('Time left in period :', scoreboard.PeriodTimeLeft)
    print(thisGame)
    #print(DD.dummyHome.Name, DD.dummyHome.TeamID)
    #frm = wx.Frame(None, title=includes.AppName)
    frm.Show()
    app.MainLoop()
    # print(includes.QueryURL)
    #print(gameDataSnapshot)

