

import time, datetime
AppName = "BL Commentator"
Version = "0.1a1"

# LastMinSkip = False     # there's an issue at iceHQ with network access to the scoreboard
# if this is set to True, the scoreboard refresh routine will skip polling the file at 61s to go.
LastMinSkip = False
LastMinSkipTimeSeconds= 61
OkToReadSBFile = True

API_URL_Base = "https://icehq.hockeysyte.com/api/"
xsyte_id = 347

# delay in seconds between polling the API - can be over-ridden
DefaultJSONRefreshInterval = int(10 * 1000) # seconds - wx Times is in miliseconds
JSONRefreshInterval = DefaultJSONRefreshInterval

DefaultScoreBoardPollIntervalMicroSeconds = int(0.5 * 1000) # seconds
ScoreBoardPollIntervalMicroSeconds = DefaultScoreBoardPollIntervalMicroSeconds

HiResScoreBoardPollIntervalMicroSeconds = int(0.1 * 1000) # seconds - we'll poll every 10th when we want hi res
# HiResScoreBoardPollIntervalMicroSeconds = int(0.5 * 1000) # 0.1 breaks at iceHQ?

SBClockLagMicroSeconds = int(0.1 * 1000)

PenDefaultPlayerName = "Marty McSorley"
PenDefaultCrime = "Gooning"

# for testing!
defaultGameID = 6551
gameID = defaultGameID

# games/game?game_id=6024&xsyte_id=347&format=json"

QueryURL = API_URL_Base + "games/game?game_id=" + str(gameID) + "&xsyte_id=" + str(xsyte_id) + "&format=json"

# ScoreBoardFile = "JSON samples/Livefeed"
ScoreBoardFile = 'JSON samples/sample_sbv3/Livefeed'

# don't use this one, it breaks the scoreboard due to read/write lock issues
# ScoreBoardFile = 'i:/Livefeedv2'

# Phill's copy file, hopefully enough to protect the main system for windows/network file locks and subsequent fuckage.
# ScoreBoardFile = 'i:/Livefeed_copy'

zerotime = datetime.time(minute=0, second=0, microsecond=0)


InitialFrameSize = (640,480)
InitialTeamFrameSize = (720,960)
# don't touch ...
LastMyTree = {}