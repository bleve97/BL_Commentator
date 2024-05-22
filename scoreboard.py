
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
        root = etree.parse(includes.ScoreBoardFile)
        with open(includes.ScoreBoardFile) as xml_file:
            xml_data = xml_file.read()

        dict_data = xmltodict.parse(xml_data)
        print(dict_data['Data'])
        type(dict_data)
        self.SBVersion = dict_data['Data']['Version']['#text']
        self.SBName = dict_data['Data']['Scoreboard']['#text']
        if dict_data['Data']['ScoreboardFields']['PeriodTime']['Running']['#text'] == 'False':
            self.PeriodStatus = False
        else:
            self.PeriodStatus = True
        # to get time left, we'll need a bit of regex magic
        self.PeriodTimeLeft = self.timeFromScoreBoard(dict_data['Data']['ScoreboardFields']['PeriodTime']['CurrentTime']['#text'])
        #self.PeriodTimeLeft = dict_data['Data']['ScoreboardFields']['PeriodTime']['CurrentTime']['#text']

        self.HomeTeamName = dict_data['Data']['ScoreboardFields']['Team1Name']['Value']['#text']
        self.AwayTeamName = dict_data['Data']['ScoreboardFields']['Team2Name']['Value']['#text']
        #print(dict_data.'Version')
        #for elem in root.iter():
        #    print(elem.tag, elem.text)

            # load up the SB fields in the object

            #self.scoreboardVersion = elem.["Version"]


    def timeFromScoreBoard(self, timeString):
        # two possibles : 19:45 - min:sec, or 55.9 sec:fraction of sec - can use the ":" or "," to make the call
        print("timeString : ", timeString)
        mins = 15
        secs = 45.0
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
                print("secs and fracs")
                mins = 0
                secs = float(m2.group(1))
                # frac = m2.group(1)
        return(mins, secs)


