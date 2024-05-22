# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# https://icehq.hockeysyte.com/api/games/game?game_id=6024&xsyte_id=347&format=json

import includes
import fetcher
#import urllib.request, json
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
    SBD = SB.ScoreBoard()  # we have Scoreboard Data, which is pulled from the scoreboard XML file
    #print(scoreboard.SBName, scoreboard.SBVersion)
    if (SBD.PeriodStatus):
        print("Period :", SBD.Period, SBD.PeriodTimeLeft)
    else:
        print("Period (paused) : ", SBD.Period, SBD.PeriodTimeLeft)
    print(SBD.HomeTeamName, ":", SBD.HomeTeamScore, " .... ", SBD.AwayTeamName, ":", SBD.AwayTeamScore)
    #print('Time left in period :', scoreboard.PeriodTimeLeft)
    print(thisGame)
    SBD.reload()    # we need to reload this every second or more. Probably every 1/2 second will do for our purposes
    #print(DD.dummyHome.Name, DD.dummyHome.TeamID)
    #frm = wx.Frame(None, title=includes.AppName)
    frm.Show()
    app.MainLoop()
    # print(includes.QueryURL)
    #print(gameDataSnapshot)

