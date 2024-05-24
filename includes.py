
AppName = "BL Commentator"
Version = "0.1a1"

API_URL_Base = "https://icehq.hockeysyte.com/api/"
xsyte_id = 347

# delay in seconds between polling the API - can be over-ridden
DefaultJSONRefreshInterval = 10
JSONRefreshInterval = DefaultJSONRefreshInterval

DefaultScoreBoardPollIntervalSeconds = 0.5 # seconds
ScoreBoardPollIntervalSeconds = DefaultScoreBoardPollIntervalSeconds

# for testing!
defaultGameID = 6024
gameID = defaultGameID

# games/game?game_id=6024&xsyte_id=347&format=json"

QueryURL = API_URL_Base + "games/game?game_id=" + str(gameID) + "&xsyte_id=" + str(xsyte_id) + "&format=json"

#ScoreBoardFile = "JSON samples/Livefeed"
ScoreBoardFile = 'JSON samples/sample_sbv3/feed'

