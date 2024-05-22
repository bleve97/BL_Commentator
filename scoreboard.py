
import includes
import time
import xml.etree.ElementTree as ET
import commclasses as CC
from lxml import etree
import xmltodict

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
        self.HomeTeamName = dict_data['Data']['ScoreboardFields']['Team1Name']['Value']['#text']
        self.AwayTeamName = dict_data['Data']['ScoreboardFields']['Team2Name']['Value']['#text']
        #print(dict_data.'Version')
        #for elem in root.iter():
        #    print(elem.tag, elem.text)

            # load up the SB fields in the object

            #self.scoreboardVersion = elem.["Version"]

