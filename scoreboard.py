import datetime

import includes
import time
import xml.etree.ElementTree as ET
import commclasses as CC
from lxml import etree
import xmltodict
import json
import re

class SBPenalty:
    def __init__(self, Number, timeLeft, crime):
        self.Number = Number
        self.timeLeft = timeLeft
        self.crime = crime




class ScoreBoard:
    def __init__(self):
        print("Opening ", includes.ScoreBoardFile)
        #root = etree.parse(includes.ScoreBoardFile)
        self.load(includes.ScoreBoardFile)


    def load(self, SBSourceFile):
        # all the shit is in here, hard coded XML parsing tags. Yuk. Yuk. Yuk.
        with open(SBSourceFile) as SB_file:
            rawSBdata = SB_file.read()
            SB_file.close()
        try:    # XML or JSON?
            dict_data = xmltodict.parse(rawSBdata)
            self.SBVersion = dict_data['Data']['Version']['#text']
            self.SBName = dict_data['Data']['Scoreboard']['#text']
            if dict_data['Data']['ScoreboardFields']['PeriodTime']['Running']['#text'] == 'False':
                self.PeriodStatus = False
            else:
                self.PeriodStatus = True

            self.Period = int(dict_data['Data']['ScoreboardFields']['Period']['Value']['#text'])
            # to get time left, we'll need a bit of regex magic
            self.PeriodTimeLeft = self.timeFromScoreBoard(
                dict_data['Data']['ScoreboardFields']['PeriodTime']['CurrentTime']['#text'])

            self.HomeTeamName = dict_data['Data']['ScoreboardFields']['Team1Name']['Value']['#text']
            self.AwayTeamName = dict_data['Data']['ScoreboardFields']['Team2Name']['Value']['#text']

            self.HomeTeamScore = dict_data['Data']['ScoreboardFields']['Team1Score']['Value']['#text']
            self.AwayTeamScore = dict_data['Data']['ScoreboardFields']['Team2Score']['Value']['#text']

            self.HomeTeamShots = dict_data['Data']['ScoreboardFields']['Team1ShotsOnGoal']['Value']['#text']
            self.AwayTeamShots = dict_data['Data']['ScoreboardFields']['Team2ShotsOnGoal']['Value']['#text']

            # penalties, the XML :
            self.HomeTeamPenalties = self.parseXMLPenalties(dict_data['Data']['ScoreboardFields']['Team1Penalties'])
            self.AwayTeamPenalties = self.parseXMLPenalties(dict_data['Data']['ScoreboardFields']['Team2Penalties'])
        except: # JSON?
            #print("it's JSON not XML! w00t!")
            SBdata = json.loads(rawSBdata)
            #print(SBdata)
            self.SBVersion = SBdata['Version']
            self.SBName = SBdata['Scoreboard']
            self.PeriodStatus = SBdata['ScoreboardFields']['PeriodTime']['Running']
            self.Period = SBdata['ScoreboardFields']['Period']['Value']
            self.PeriodTimeLeft = self.timeFromScoreBoard(SBdata['ScoreboardFields']['PeriodTime']['CurrentTime'])
            self.HomeTeamName = SBdata['ScoreboardFields']['Team1Name']['Value']
            self.HomeTeamScore = SBdata['ScoreboardFields']['Team1Score']['Value']
            self.HomeTeamShots = SBdata['ScoreboardFields']['Team1ShotsOnGoal']['Value']
            self.AwayTeamName = SBdata['ScoreboardFields']['Team2Name']['Value']
            self.AwayTeamScore = SBdata['ScoreboardFields']['Team2Score']['Value']
            self.AwayTeamShots = SBdata['ScoreboardFields']['Team2ShotsOnGoal']['Value']

            # print(SBdata['ScoreboardFields']['Team2Penalties'])

            self.HomeTeamPenalties = self.parseJSONPenalties(SBdata['ScoreboardFields']['Team1Penalties']['Penalties'])
            self.AwayTeamPenalties = self.parseJSONPenalties(SBdata['ScoreboardFields']['Team2Penalties']['Penalties'])



    def reload(self):
        # regrab everything from the XML, including a reopen of the file
        #print("reloading from XML")
        self.load(includes.ScoreBoardFile)

    def parseJSONPenalties(self, chunk):
        #print("parsing :", chunk)
        Penalties = []
        penaltyCounter = len(chunk)
        #print("penalty Counter :", penaltyCounter)
        if len(chunk) > 0:  # if there's any penalties in the XML
            #print(chunk)
            #loop over penalties and create SBPenalty objects
            for penalty in chunk:
                #print(penalty)
                number = penalty['PlayerNumber']['Value']
                timeLeft = penalty['PenaltyTime']['CurrentTime']  # ['PenaltyTime']['Value']['#text']
                # print("penalty to ", number, timeLeft)

                crime = False
                thisPen = SBPenalty(Number = int(number), timeLeft = timeLeft, crime = crime)
                Penalties.append(thisPen)
        else:
            Penalties = False
        return Penalties

    def parseXMLPenalties(self, chunk):
        print("parsing :", chunk)
        Penalties = []
        if len(chunk['Penalties']) > 1: # if there's any penalties in the XML
            print(chunk['Penalties'])
            # loop over penalties and create SBPenalty objects
            for penalty in chunk['Penalties']['Item']:
                print(penalty)
                number = penalty['PlayerNumber']['Value']['#text']
                timeLeft = penalty['PenaltyTime']['CurrentTime']['#text'] # ['PenaltyTime']['Value']['#text']
                #print("penalty to ", number, timeLeft)

                crime = False
                #thisPen = SBPenalty(Number = int(number), timeLeft = timeLeft, crime = crime)
                #Penalties.append(thisPen)
        else:
            Penalties = False
        return Penalties


    def timeFromScoreBoard(self, timeString):
        # two possibles : 19:45 - min:sec, or 55.9 sec:fraction of sec - can use the ":" or "," to make the call
        #print("timeString : ", timeString)
        mins = 99
        secs = 61
        msec = 0
        p = re.compile(r'(\d+)\:(\d+)')
        m = p.match(timeString)
        if (m):
            mins = int(m.group(1))
            secs = int(m.group(2))

        else:
            p2 = re.compile(r'(\d+)\.(\d)')
            m2 = p2.match(timeString)
            if (m2):
                #print("secs and fracs")
                mins = 0
                secs = int(m2.group(1))
                msec = int(m2.group(2)) * 100000
        SBtime = datetime.time(minute=mins, second=secs, microsecond=msec)
        #print(SBtime)
        return(SBtime)


