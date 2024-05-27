#Initialise
import xml.etree.ElementTree as ET

CurrentTime = "20:00"
CurrentPeriod = "P1"
PreviousCurrentTime = "."
PreviousTeam1Name = "."
PreviousTeam1Score = "0"
PreviousTeam1ShotsOnGoal = "0"
PreviousTeam2Name = "."
PreviousTeam2Score = "0"
PreviousTeam2ShotsOnGoal = "0"
Team1Name = "0"
Team1Score = "0"
Team1ShotsOnGoal = "0"
Team2Name = "0"
Team2Score = "0"
Team2ShotsOnGoal = "0"
state="."
PreviousPeriod="."

currentNoPP=""
currentNeutralPP=""
currentNeutralPPclock=""
currentAwayPP=""
currentAwayPPclock=""
currentHomePP=""
currentHomePPclock=""

Team2PenaltyCount = 0

import time

#print(myroot[0].tag)
#print(myroot[1].tag)
#print(myroot[2][0][0].tag)

while CurrentTime != "NEVERSTOP": #will never stop conditon is not ment to meet
    time.sleep(0.005)
    try:
        mytree = ET.parse('C:\TEMP\Scoreboard Output\Livefeedv2')
        myroot = mytree.getroot()
        #CURRENT TIME
        for x in myroot[2].findall('PeriodTime'):
            CurrentTime =x.find('CurrentTime').text

        #CURRENT PERIOD
        for x in myroot[2].findall('Period'):
            Period =x.find('Value').text
            if Period == "1":
                CurrentPeriod = "P1"
            if Period == "2":
                CurrentPeriod = "P2"
            if Period == "3":
                CurrentPeriod = "P3"
            if Period == "o":
                CurrentPeriod = "OT"

        #TEAM 1 ITEMS
        for x in myroot[2].findall('Team1Name'):
            Team1Name =x.find('Value').text
            
        for x in myroot[2].findall('Team1Score'):
            if x.find('Value').text != "":
                Team1Score =x.find('Value').text
            
        for x in myroot[2].findall('Team1ShotsOnGoal'):
            if x.find('Value').text != "":
                Team1ShotsOnGoal =x.find('Value').text
            

        #TEAM 2 ITEMS    
        for x in myroot[2].findall('Team2Name'):
            Team2Name =x.find('Value').text
            
        for x in myroot[2].findall('Team2Score'):
            if x.find('Value').text != "":
                Team2Score =x.find('Value').text
            
        for x in myroot[2].findall('Team2ShotsOnGoal'):
            if x.find('Value').text != "":
                Team2ShotsOnGoal =x.find('Value').text


        #Penalties
        #Team 1
        PenaltyLowestTime = "5:00"
        Team1PenaltyCount = 0
        for x in myroot[2].findall('Team1Penalties'):
            for y in x[0].findall('Item'):
                PenaltyCurrentTime = y.find('PenaltyTime').find('CurrentTime').text
                Team1PenaltyCount +=1  #Keeps count of Team 1 Penalties
                try:
                    if PenaltyCurrentTime < PenaltyLowestTime:
                        PenaltyLowestTime = PenaltyCurrentTime    #Identifies the lowest Clock
                except:
                    print("Penalty Error", CurrentTime,  PenaltyLowestTime, PenaltyCurrentTime)

        #Team 2
        Team2PenaltyCount = 0
        for x in myroot[2].findall('Team2Penalties'):
            for y in x[0].findall('Item'):
                PenaltyCurrentTime = y.find('PenaltyTime').find('CurrentTime').text
                Team2PenaltyCount +=1  #Keeps count of Team 2 Penalties
                try:
                    if PenaltyCurrentTime < PenaltyLowestTime:
                        PenaltyLowestTime = PenaltyCurrentTime    #Identifies the lowest Clock
                except:
                    print("Penalty Error", CurrentTime,  PenaltyLowestTime, PenaltyCurrentTime)

        #Penalty Checks
        #No Penalties
        if Team1PenaltyCount + Team2PenaltyCount == 0:
            try: 
                NoPP=""
                NeutralPP=""
                NeutralPPclock=""
                AwayPP=""
                AwayPPclock=""
                HomePP=""
                HomePPclock=""
                
            except:
                print("Var Update Error", CurrentTime)

            #Neutral Penalties
        if Team1PenaltyCount == Team2PenaltyCount and Team1PenaltyCount > 0:
            if Team1PenaltyCount == 1:
                state="4 v4"
            if Team1PenaltyCount >= 2 and Team2PenaltyCount >= 2:
                state="3 v3"
            try:
                NoPP="FALSE"
                NeutralPP=state
                NeutralPPclock=PenaltyLowestTime
                AwayPP=""
                AwayPPclock=""
                HomePP=""
                HomePPclock=""

            except:
                print("Var Update Error", CurrentTime)
                
            #Home PP
        if Team1PenaltyCount < Team2PenaltyCount:
            if Team2PenaltyCount == 1:
                state=Team1Name + " PP"
            if Team2PenaltyCount >= 2 and Team1PenaltyCount == 1:
                state=Team1Name + " 4 v3"
            if Team2PenaltyCount >= 2 and Team1PenaltyCount == 0:
                state=Team1Name + " 5 v3"
            try:
                NoPP="FALSE"
                NeutralPP=""
                NeutralPPclock=""
                AwayPP=""
                AwayPPclock=""
                HomePP=state
                HomePPclock=PenaltyLowestTime

            except:
                print("Var Update Error", CurrentTime)
        
            #Away PP
        if Team1PenaltyCount > Team2PenaltyCount:
            if Team1PenaltyCount == 1:
                state=Team2Name + " PP"
            if Team1PenaltyCount >= 2 and Team2PenaltyCount == 1:
                state=Team2Name + " 4 v3"
            if Team1PenaltyCount >= 2 and Team2PenaltyCount == 0:
                state=Team2Name + " 5 v3"
            try:
                NoPP="FALSE"
                NeutralPP=""
                NeutralPPclock=""
                AwayPP=state
                AwayPPclock=PenaltyLowestTime
                HomePP=""
                HomePPclock=""
                
            except:
                print("WRITE Error", CurrentTime)
                
        #print("PENALTY TIME = ",PenaltyLowestTime)
        #print("PENALTY COUNT Team1 = ",Team1PenaltyCount)
        #print("PENALTY COUNT Team2 = ",Team2PenaltyCount)

        #File Print
        if(PreviousCurrentTime != CurrentTime):
            f = open("TIME.txt", "wt")
            f.write(CurrentTime.split('.')[0])
            f.close()

        if(PreviousPeriod != CurrentPeriod):
            f = open("PERIOD.txt", "wt")
            f.write(CurrentPeriod)
            f.close()
            
        if(PreviousTeam1Name != Team1Name):
            f = open("Team1Name.txt", "wt")
            f.write(Team1Name)
            f.close()

        if(PreviousTeam1Score != Team1Score):    
            f = open("Team1Score.txt", "wt")
            f.write(Team1Score)
            f.close()

        if(PreviousTeam1ShotsOnGoal != Team1ShotsOnGoal):
            f = open("Team1ShotsOn.txt", "wt")
            #f.write("SHOTS ")
            f.write(Team1ShotsOnGoal)
            f.close()

        if(PreviousTeam2Name != Team2Name):
            f = open("Team2Name.txt", "wt")    
            f.write(Team2Name)
            f.close()

        if(PreviousTeam2Score != Team2Score):
            f = open("Team2Score.txt", "wt")    
            f.write(Team2Score)
            f.close()

        if(PreviousTeam2ShotsOnGoal != Team2ShotsOnGoal):
            f = open("Team2ShotsOn.txt", "wt")    
            #f.write("SHOTS ")
            f.write(Team2ShotsOnGoal)
            f.close()

        if(NoPP != currentNoPP):
            f = open("NoPP.txt", "wt")    
            f.write(NoPP)
            f.close()
            currentNoPP = NoPP

        if(NeutralPP != currentNeutralPP):
            f = open("NeutralPPstate.txt", "wt")    
            f.write(NeutralPP)
            f.close()
            currentNeutralPP = NeutralPP

        if(AwayPP != currentAwayPP):
            f = open("AwayPPstate.txt", "wt")    
            f.write(AwayPP)
            f.close()
            currentAwayPP = AwayPP

        if(HomePP != currentHomePP):
            f = open("HomePPstate.txt", "wt")    
            f.write(HomePP)
            f.close()
            currentHomePP = HomePP

        if(NeutralPPclock != currentNeutralPPclock):
            f = open("NeutralPPclock.txt", "wt")    
            f.write(NeutralPPclock)
            f.close()
            currentNeutralPPclock = NeutralPPclock

        if(AwayPPclock != currentAwayPPclock):
            f = open("AwayPPclock.txt", "wt")    
            f.write(AwayPPclock)
            f.close()
            currentAwayPPclock = AwayPPclock

        if(HomePPclock != currentHomePPclock):
            f = open("HomePPclock.txt", "wt")    
            f.write(HomePPclock)
            f.close()
            currentHomePPclock = HomePPclock

        #Screen Print for Debug        
        #print("TIME = ",CurrentTime)
        #print(Team1Name, "Score = ", Team1Score, "Shots On = ", Team1ShotsOnGoal)
        #print(Team2Name, "Score = ", Team2Score, "Shots On = ", Team2ShotsOnGoal)

        #Set Old Value for updateCheck
        PreviousCurrentTime =  CurrentTime
        PreviousTeam1Name = Team1Name
        PreviousTeam1Score = Team1Score
        PreviousTeam1ShotsOnGoal = Team1ShotsOnGoal
        PreviousTeam2Name = Team2Name
        PreviousTeam2Score = Team2Score
        PreviousTeam2ShotsOnGoal = Team2ShotsOnGoal
        PreviousPeriod = CurrentPeriod
    except:
        print("File Read ERROR", CurrentTime)
        
