import datetime

import includes
import time
import xml.etree.ElementTree as ET
import commclasses as CC
from lxml import etree
#import xmltodict
import xml.etree.ElementTree as ET
import json
import re

#self.OkToReadFile = True

class SBPenalty:
    def __init__(self, Number, timeLeft, crime, duration = 120):
        self.Number = Number
        self.timeLeft = timeLeft
        self.duration = duration
        self.crime = crime




class ScoreBoard:
    def __init__(self):
        print("Opening ", includes.ScoreBoardFile)
        #root = etree.parse(includes.ScoreBoardFile)

        self.load(includes.ScoreBoardFile)
        print("opened")
        #self.OkToReadFile = True


    def load(self, SBSourceFile):
        # all the shit is in here, hard coded XML parsing tags. Yuk. Yuk. Yuk.
        try:
            if includes.OkToReadSBFile == True:
                with open(SBSourceFile) as SB_File:
                    mytree = ET.parse(SB_File)
                    includes.LastMyTree = mytree
                    SB_File.close()
            else:
                mytree = includes.LastMyTree
                print("iceHQ network bug workaround active, skipping file read")

            dict_data = mytree.getroot()    # this could fail if the prog starts without being able to read the file

            self.SBVersion = dict_data[1].text
            self.SBName = dict_data[0].text

            #print("myroot :", dict_data[2].findall('Period').text)
            for x in dict_data[2].findall('PeriodTime'):
                self.PeriodTimeLeft = self.timeFromScoreBoard(x.find('CurrentTime').text)
                #print(self.PeriodTimeLeft)
                if (x.find('Running').text == "True"):
                    self.PeriodStatus = True
                else:
                    self.PeriodStatus = False
                    # if it's not running, we need to skip lots
                #print('Running? : ', self.PeriodStatus)

            # CURRENT PERIOD
            if (self.PeriodStatus):
                for x in dict_data[2].findall('Period'):
                    Period = x.find('Value').text
                    if Period == "1":
                        self.Period = 1
                    if Period == "2":
                        self.Period = 2
                    if Period == "3":
                        self.Period = 3
                    if Period == "E":
                        self.Period = "OT"
            else:
                self.Period = 0
            # TEAM 1 ITEMS
            for x in dict_data[2].findall('Team1Name'):
                self.HomeTeamName = x.find('Value').text

            for x in dict_data[2].findall('Team1Score'):
                if x.find('Value').text != "":
                    self.HomeTeamScore = x.find('Value').text
            if not self.HomeTeamScore:
                self.HomeTeamScore = 0

            for x in dict_data[2].findall('Team1ShotsOnGoal'):
                if x.find('Value').text != "":
                    self.HomeTeamShots = x.find('Value').text
            if not self.HomeTeamShots:
                self.HomeTeamShots = 0
            # TEAM 2 ITEMS
            for x in dict_data[2].findall('Team2Name'):
                self.AwayTeamName = x.find('Value').text
            for x in dict_data[2].findall('Team2Score'):
                if x.find('Value').text != "":
                    self.AwayTeamScore = x.find('Value').text
            if not self.AwayTeamScore:
                self.AwayTeamScore = 0
            for x in dict_data[2].findall('Team2ShotsOnGoal'):
                if x.find('Value').text != "":
                   self.AwayTeamShots = x.find('Value').text
            if not self.AwayTeamShots:
                self.AwayTeamShots = 0
            # penalties, the XML :

            self.HomeTeamPenalties = self.parseXMLPenalties(dict_data[2].findall('Team1Penalties'))
            self.AwayTeamPenalties = self.parseXMLPenalties(dict_data[2].findall('Team2Penalties'))

        except Exception as error: # JSON?
            print(error)
            #print("JSON?")
            exit()
            #print("it's JSON not XML! w00t!")
            SBdata = json.loads(rawSBdata)
            #print(SBdata)
            self.SBVersion = SBdata['Version']
            self.SBName = SBdata['Scoreboard']
            self.PeriodStatus = SBdata['ScoreboardFields']['PeriodTime']['Running']
            self.Period = int(SBdata['ScoreboardFields']['Period']['Value'])
            self.PeriodTimeLeft = self.timeFromScoreBoard(SBdata['ScoreboardFields']['PeriodTime']['CurrentTime'])
            self.HomeTeamName = SBdata['ScoreboardFields']['Team1Name']['Value']
            self.HomeTeamScore = int(SBdata['ScoreboardFields']['Team1Score']['Value'])
            self.HomeTeamShots = int(SBdata['ScoreboardFields']['Team1ShotsOnGoal']['Value'])
            self.AwayTeamName = SBdata['ScoreboardFields']['Team2Name']['Value']
            self.AwayTeamScore = int(SBdata['ScoreboardFields']['Team2Score']['Value'])
            self.AwayTeamShots = int(SBdata['ScoreboardFields']['Team2ShotsOnGoal']['Value'])

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
        # print("parsing XML chunk:", chunk)
        # print("tags :", chunk[0].tag, chunk[0].attrib)
        Penalties = []

        for y in chunk[0]:
            # print("looping on y", y.tag, y.attrib)
            # print("bar :", y.findall('PenaltyTime'))
            for child in y:
                # print(child.tag, child.attrib)
                PenaltyCurrentTime = child.find('PenaltyTime').find('CurrentTime').text
                PenaltyPlayerNumber = child.find('PlayerNumber').find('Value').text
                # print("PCT: ", PenaltyCurrentTime, "to :", PenaltyPlayerNumber)
                crime = False
                thisPen = SBPenalty(Number = int(PenaltyPlayerNumber), timeLeft = PenaltyCurrentTime, crime = crime)
                Penalties.append(thisPen)
        # else:
            # print("no penalty")
            # Penalties = False
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
        # iceHQ file access hack, urk ...
        #print(SBtime, includes.LastMinSkipTime)
        #print(SBtime.minute, SBtime.second)
        #print(includes.LastMinSkipTime.minute, includes.LastMinSkipTime.second)
        SBTimeSeconds = (SBtime.minute * 60) + SBtime.second
        # print("SBTimeSeconds : ", SBTimeSeconds)

        #timeDiff = SBtime - includes.LastMinSkipTime
        #print(timeDiff)
        if (SBTimeSeconds <= includes.LastMinSkipTimeSeconds): #  and (includes.LastMinSkip):
            includes.OkToReadSBFile = False
        else:
            includes.OkToReadSBFile = True
        # hack to check logic
        #includes.OkToReadSBFile = False
        #print(SBtime)
        return(SBtime)


