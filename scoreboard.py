
import includes
import time
import xml.etree.ElementTree as ET
import commclasses as CC
from lxml import etree
import xmltodict
import re

class ScoreBoard:
    def __init__(self):
        print("Opening ", includes.ScoreBoardFile)
        #root = etree.parse(includes.ScoreBoardFile)
        self.load(includes.ScoreBoardFile)


    def load(self, xmlSourceFile):
        # all the shit is in here, hard coded XML parsing tags. Yuk. Yuk. Yuk.
        with open(xmlSourceFile) as xml_file:
            xml_data = xml_file.read()
            xml_file.close()

        dict_data = xmltodict.parse(xml_data)
        # print(dict_data['Data'])
        # type(dict_data)
        self.SBVersion = dict_data['Data']['Version']['#text']
        self.SBName = dict_data['Data']['Scoreboard']['#text']
        if dict_data['Data']['ScoreboardFields']['PeriodTime']['Running']['#text'] == 'False':
            self.PeriodStatus = False
        else:
            self.PeriodStatus = True

        self.Period = int(dict_data['Data']['ScoreboardFields']['Period']['Value']['#text'])
        # to get time left, we'll need a bit of regex magic
        self.PeriodTimeLeft = self.timeFromScoreBoard(dict_data['Data']['ScoreboardFields']['PeriodTime']['CurrentTime']['#text'])

        self.HomeTeamName = dict_data['Data']['ScoreboardFields']['Team1Name']['Value']['#text']
        self.AwayTeamName = dict_data['Data']['ScoreboardFields']['Team2Name']['Value']['#text']

        self.HomeTeamScore = dict_data['Data']['ScoreboardFields']['Team1Score']['Value']['#text']
        self.AwayTeamScore = dict_data['Data']['ScoreboardFields']['Team2Score']['Value']['#text']

        self.HomeTeamShots = dict_data['Data']['ScoreboardFields']['Team1ShotsOnGoal']['Value']['#text']
        self.AwayTeamShots = dict_data['Data']['ScoreboardFields']['Team2ShotsOnGoal']['Value']['#text']

    def reload(self):
        # regrab everything from the XML, including a reopen of the file
        #print("reloading from XML")
        self.load(includes.ScoreBoardFile)


    def timeFromScoreBoard(self, timeString):
        # two possibles : 19:45 - min:sec, or 55.9 sec:fraction of sec - can use the ":" or "," to make the call
        #print("timeString : ", timeString)
        mins = 99
        secs = 61.0
        frac = 0
        p = re.compile(r'(\d+)\:(\d+)')
        m = p.match(timeString)
        if (m):
            mins = int(m.group(1))
            secs = float(m.group(2))

        else:
            p2 = re.compile(r'(\d+)\.(\d)')
            m2 = p2.match(timeString)
            if (m2):
                #print("secs and fracs")
                mins = 0
                secs = float(m2.group())
        return(mins, secs)


