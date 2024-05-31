

import time, datetime
AppName = "BL Commentator"
Version = "0.1a1"

API_URL_Base = "https://icehq.hockeysyte.com/api/"
xsyte_id = 347

# delay in seconds between polling the API - can be over-ridden
DefaultJSONRefreshInterval = int(10 * 1000) # seconds - wx Times is in miliseconds
JSONRefreshInterval = DefaultJSONRefreshInterval

DefaultScoreBoardPollIntervalSeconds = int(0.5 * 1000) # seconds
ScoreBoardPollIntervalSeconds = DefaultScoreBoardPollIntervalSeconds
# HiResScoreBoardPollIntervalSeconds = int(0.1 * 1000) # seconds - we'll poll every 10th when we want hi res
HiResScoreBoardPollIntervalSeconds = int(0.5 * 1000) # 0.1 breaks at iceHQ?

PenDefaultPlayerName = "Marty McSorley"
PenDefaultCrime = "Gooning"

# for testing!
defaultGameID = 6548
gameID = defaultGameID

# games/game?game_id=6024&xsyte_id=347&format=json"

QueryURL = API_URL_Base + "games/game?game_id=" + str(gameID) + "&xsyte_id=" + str(xsyte_id) + "&format=json"

# ScoreBoardFile = "JSON samples/Livefeed"
# ScoreBoardFile = 'JSON samples/sample_sbv3/Livefeed'
ScoreBoardFile = 'i:/Livefeedv2'

zerotime = datetime.time(minute=0, second=0, microsecond=0)
