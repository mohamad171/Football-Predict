from mongoengine import *

connect("AmarFootballiORM",host="localhost",port=8085)

class TeamsData(Document):
    TeamName = StringField(required=True)
    FaTeamName = StringField(required=True)
    TeamImage = StringField(required=True)
    Group = StringField(required=True)
class MatchData(Document):
    HomeTeam = ReferenceField(TeamsData,required=True)
    AwayTeam = ReferenceField(TeamsData,required=True)
    Group = StringField(required=True)
    Date = StringField(required=True)
    Time = StringField(required=True)
    MatchStadium = StringField(required=True)    
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