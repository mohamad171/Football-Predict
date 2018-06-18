from . import DBModel
from . import jalali
import datetime
import time

class WorlCup:
    def GetMainData(self,group):
        matcharr = []
        videoarr = []
        
        groupname = group
        matchdata = DBModel.MatchData.objects(Group = groupname)
        for l in matchdata:
            # tim = time.strftime(l.Time, '%I:%M')
            # tim = time.struct_time(tm_hour=13, tm_min=33)
            # print(tim + datetime.timedelta(hours=1))
            # str_date = l.Time
            # from datetime import datetime
            # date_date = datetime.strftime(str_date, "%H:%M")
            querydata = {
            "MatchId":str(l.id),
            "HomeTeamName":l.HomeTeam.FaTeamName,
            "AwayTeamName":l.AwayTeam.FaTeamName,
            "HomeTeamImage":l.HomeTeam.TeamImage,
            "AwayTeamImage":l.AwayTeam.TeamImage,
            # "FaTime": l.Time + datetime.timedelta(minutes = 10),
            "FaDate": jalali.Gregorian(l.Date).persian_string(),
            "Date": l.Date,
            "Time": l.Time,
            "Stadium": l.MatchStadium
        }
            matcharr.append(querydata)
        matchresults = DBModel.MatchResults.objects()
        try:
            for h in matchresults:
                matchdata = DBModel.MatchData.objects(id = h.Match.id).get()
                videodata = DBModel.VideoData.objects(Match=matchdata).get()
                if(matchdata.Group == groupname):
                    videoquery={
            "MatchId":str(matchdata.id),
            "HomeTeamName":matchdata.HomeTeam.FaTeamName,
            "AwayTeamName":matchdata.AwayTeam.FaTeamName,
            "HomeTeamImage":matchdata.HomeTeam.TeamImage,
            "AwayTeamImage":matchdata.AwayTeam.TeamImage,
            "HomeGoals": h.HomeGoals,
            "AwayGoals": h.AwayGoals,
            "Description": videodata.Description,
            "VideoUrl": videodata.VideoUrl

        }
                    videoarr.append(videoquery)
        except Exception as e:
            print("Exception:"+str(e))
            videoarr = []
        return matcharr , videoarr


    def GetGroupTable(self,group):
        teamsarr = []
        finalarr = []
        groupname = group
        teamsdata = DBModel.TeamsData.objects(Group = groupname)
        for l in teamsdata:
            counter = 0
            leaguetable = DBModel.GroupTable.objects(TeamName=l).get()
            objdata = {
            "TeamName": leaguetable.TeamName.FaTeamName,
            "TeamImage": l.TeamImage,
            "GoalsRecived": leaguetable.GoalsRecived,
            "Goals": leaguetable.Goals,
            "TotalGoals": leaguetable.TotalGoals,
            "NumberOfMatches": leaguetable.NumberOfMatches,
            "Score": leaguetable.Score if leaguetable.Score > 0 else 0,
        }
            if counter == 0:
                teamsarr.append(objdata)
            else:   
                for h in teamsarr:
                    if h.TeamName != objdata["TeamName"]:
                        teamsarr.append(objdata)
                    counter += 1
        teamsarr = sorted(teamsarr, key=lambda d: d["Score"],reverse=True)            
        return teamsarr              
           



    def SetVideo(self,match,url,description):
        videomodel = DBModel.VideoData()
        videomodel.Match = match
        videomodel.Description = description
        videomodel.VideoUrl = url
        videomodel.save()
        
    def SetGroupTable(self,match):
#      result = DBModel.MatchResults.objects(Match=match)
        matchresults = DBModel.MatchResults.objects(Match=match).get()
        if matchresults.isSet == 0:
            grouptable = DBModel.GroupTable.objects(TeamName=matchresults.Match.HomeTeam).get()
            grouptable.TotalGoals = grouptable.Goals + (matchresults.HomeGoals - matchresults.AwayGoals)
            grouptable.GoalsRecived = matchresults.AwayGoals
            grouptable.Goals = matchresults.HomeGoals
            grouptable.NumberOfMatches = grouptable.NumberOfMatches + 1
            if matchresults.WinnerTeam == "h":
                grouptable.Score = grouptable.Score + 3
            elif matchresults.WinnerTeam == "a":
                grouptable.Score = grouptable.Score - 3
            elif  matchresults.WinnerTeam == "d":
                grouptable.Score = grouptable.Score + 1
            matchresults.isSet = 1    
            grouptable.save()
        
        #################################################
            grouptable = DBModel.GroupTable.objects(TeamName=matchresults.Match.AwayTeam).get()
            grouptable.TotalGoals = grouptable.Goals + (matchresults.AwayGoals - matchresults.HomeGoals)
            grouptable.NumberOfMatches = grouptable.NumberOfMatches + 1
            grouptable.GoalsRecived = matchresults.HomeGoals
            grouptable.Goals = matchresults.AwayGoals
            if matchresults.WinnerTeam == "h":
                grouptable.Score = grouptable.Score - 3
            elif matchresults.WinnerTeam == "a":
                grouptable.Score = grouptable.Score + 3
            elif  matchresults.WinnerTeam == "d":
                grouptable.Score = grouptable.Score + 1
            grouptable.save()
            matchresults.isSet = 1
            matchresults.save()
            return "ok"         
    def SetMatchResult(self,match,homegoals,awaygoals):
        results = DBModel.MatchResults()
        results.Match = match
        results.HomeGoals = homegoals
        results.AwayGoals = awaygoals
        results.isSet = 0
        if homegoals > awaygoals:
            results.WinnerTeam = "h"
        elif homegoals == awaygoals:
            results.WinnerTeam = "d"
        elif homegoals < awaygoals:
            results.WinnerTeam = "a"
        results.save()
        
        return "ok"