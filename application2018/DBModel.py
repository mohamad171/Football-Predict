from mongoengine import *


connect("AmarFootballi2018",host="localhost",port=2017)

class LeaguesData(Document):
    LeagueName = StringField(required=True)
    LegaueTeamsCount = IntField(required=True)
    LeagueSeason = StringField(required=True)
    LeagueLogoUrl = StringField(required=True)
    LeagueMaxMatches = IntField(required=True)
    LeagueCurrentMatchDay = IntField(required=True)
class TeamsData(Document):
    TeamName = StringField(required=True)
    FaTeamName = StringField(required=True)
    TeamImage = StringField(required=True)
    League = ReferenceField(LeaguesData,required=True)
class MatchData(Document):
    HomeTeam = ReferenceField(TeamsData,required=True)
    AwayTeam = ReferenceField(TeamsData,required=True)
    League = ReferenceField(LeaguesData,required=True)
    Date = StringField(required=True)
    Time = StringField(required=True)
class GroupTable(Document):
    TeamName = ReferenceField(TeamsData,required=True)
    GoalsRecived = IntField(required = True)
    Goals = IntField(required = True)
    TotalGoals= IntField(required=True)
    NumberOfMatches = IntField(required=True)
    Score = IntField(required=True)
class MatchResults(Document):
    Match = ReferenceField(MatchData,required=True)
    HomeGoals = IntField(required=True)
    AwayGoals = IntField(required=True)
    HomePosition = IntField(required=True)
    AwayPosition = IntField(required=True)
    HomeYellowCard = IntField(required=True)
    AwayYellowCard = IntField(required=True)
    HomeRedCarde = IntField(required=True)
    AwayRedCard = IntField(required=True)
    HomePasses = IntField(required=True)
    AwayPasses = IntField(required=True)
    HomeCorners = IntField(required=True)
    AwayCorners = IntField(required=True)
    WinnerTeam = StringField(required=True)
    isSet = IntField(required=True)
class UsersData(Document):
    DeviceId = StringField(required=True)
    Fname = StringField()
    Lname = StringField()
    PhoneNumber = StringField()    
class VideoData(Document):
    Match = ReferenceField(MatchData,required=True)
    Description = StringField()
    VideoUrl = StringField(required=True)