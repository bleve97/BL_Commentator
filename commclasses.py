from typing import Optional
from typing import List, Dict, Any
from sqlalchemy import ForeignKey
import sqlalchemy
from sqlalchemy import String, types
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship, Session
import enum

BL_CommClassesVersion = 0.1

print("SQLAlchemy v", sqlalchemy.__version__, "BL_CommClassesVersion :", BL_CommClassesVersion)
#engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)
engine = create_engine("sqlite+pysqlite:///database/commentator.db", echo=True)

session = Session(engine)
# print(session)
class Base(DeclarativeBase):
    pass


class GameState(enum.Enum):
    PENDING = "pending"
    Period1 = "period 1"
    Period2 = "period 2"
    Period3 = "period 3"
    Overtime = "overtime"
    Shootout = "shootout"
    Completed = "completed"
    Intermission = "intermission"


class Position(enum.Enum):
    Forward = "forward"
    Defence = "defence"
    Goalie = "goalie"

class ForwardType(enum.Enum):
    Wing = "wing"
    Center = "center"

class PositionSide(enum.Enum):
    Left = "left"
    Right = "right"

class Team(Base):
    __tablename__ = "teams"
    TeamID: Mapped[int] = mapped_column(primary_key=True)
    xciteTeamID: Mapped[Optional[int]]
    Name: Mapped[str]
    ShortName: Mapped[Optional[str]]
    BaseColour: Mapped[Optional[str]] # this will be of the form ffaa33 etc, for RGB values
    TextColour: Mapped[Optional[str]] # same as for BaseColour

    LogoURL: Mapped[Optional[str]]
    GoalVideo: Mapped[Optional[str]]
    GoalHorn: Mapped[Optional[str]]
    WarmupPlaylist: Mapped[Optional[str]]
    WinSong: Mapped[Optional[str]]
    HomePage: Mapped[Optional[str]]

    #staffers: Mapped[List["StaffMember"]] = relationship(back_populates="Team")
    #players: Mapped[List["Player"]] = relationship(back_populates="Team")

class Game(Base):
    __tablename__ = "games"
    GameID: Mapped[int] = mapped_column(primary_key=True)
    xciteGameID: Mapped[Optional[int]]  # not every game is in hockeysyte?

    State: Mapped[GameState]
    LastState: Mapped[GameState]
    OvertimeCount: Mapped[int]

    HomeTeamID: Mapped[int] = mapped_column(ForeignKey("teams.TeamID"))
    #AwayTeamID: Mapped[Team]
    HomeScore: Mapped[int]
    AwayScore: Mapped[int]
    HomeShots: Mapped[Optional[int]]
    AwayShots: Mapped[Optional[int]]
    HomePIM: Mapped[Optional[int]]
    AwayPIM: Mapped[Optional[int]]

    #def __repr__(self) -> str:
    #    return f"Game(id={self.GameID})"








class Player(Base):
    __tablename__ = "players"
    PlayerID: Mapped[int] = mapped_column(primary_key=True)
    FirstName: Mapped[str] = mapped_column(String(30))
    SirName: Mapped[str] = mapped_column(String(30))
    PronunciationGuide: Mapped[Optional[str]] = mapped_column(String(50))
    Number: Mapped[int]
    GameNumber : Mapped[int] # not always the same as their normal number, can be changed etc
    GamePIM: Mapped[int]
    GameGoals: Mapped[int]
    GameAssists: Mapped[int]
    StartingPosition: Mapped[Position]
    CurrentPosition: Mapped[Position]
    PositionSide: Mapped[PositionSide]
    ForwardType: Mapped[ForwardType]

    xcitePlayerID: Mapped[int]
    #Team: Mapped["Team"] = relationship(back_populates="players")

    def GetPlayerByNumber(self, number):
        print("looking for Player No. ", number)
        return False    # if no match



class StaffMember(Base):
    __tablename__ = "staffmembers"
    StaffID: Mapped[int] = mapped_column(primary_key=True)
    FirstName: Mapped[str] = mapped_column(String(30))
    Sirname: Mapped[str] = mapped_column(String(30))
    PronunciationGuide: Mapped[Optional[str]] = mapped_column(String(50))
    Role: Mapped[str] # coach, ac, manager
    #Team: Mapped["Team"] = relationship(back_populates="staffers")
class Goal(Base):
    __tablename__ = "goals"
    GoalID: Mapped[int] = mapped_column(primary_key=True)



class Penalty(Base):
    __tablename__ = "penalties"
    PenaltyID: Mapped[int] = mapped_column(primary_key=True)
    timeLeft = 0 # we get this from the scoreboard
    # Player


class Shot(Base):
    __tablename__ = "shots"
    ShotID: Mapped[int] = mapped_column(primary_key=True)


class Period(Base):
    __tablename__ = "periods"
    PeriodID: Mapped[int] = mapped_column(primary_key=True)


## initialise all the stuff we need. These will basically be globals
Base.metadata.create_all(engine)
ThisGame = Game()
HomeTeam = Team(Name="homers")
AwayTeam = Team(Name="awayers")