from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from pymongo import MongoClient
from django.views.decorators.csrf import csrf_exempt
from application2018 import DBModel
from pymongo import MongoClient
from bson import json_util

client = MongoClient('mongodb://localhost:27017/')

@csrf_exempt 
def panelindex(request):
    
    template = loader.get_template("website/index.html")
    return HttpResponse(template.render())

@csrf_exempt 
def leagues(request):
    
    if request.method == "POST":
        leagues = DBModel.LeaguesData()
        leaguename = request.POST.get("leaguename")
        teamscount = request.POST.get("teamscount")
        seaseon = request.POST.get("seaseon")
        matchescount = request.POST.get("matchescount")
        logourl = request.POST.get("logourl")
        leagues.LeagueName = leaguename
        leagues.LegaueTeamsCount = int(teamscount)
        leagues.LeagueSeason = seaseon
        leagues.LeagueLogoUrl = logourl
        leagues.LeagueMaxMatches = matchescount
        leagues.LeagueCurrentMatchDay = 1
        leagues.IsActive = True
        leagues.save()



    leaguesdata = []
    leagesarr = DBModel.LeaguesData.objects()
    for l in leagesarr:
        jso={
            "LeagueName": l.LeagueName,
            "LegaueTeamsCount": l.LegaueTeamsCount,
            "LeagueSeason": l.LeagueSeason,
            "LeagueMaxMatches": l.LeagueMaxMatches,
            "LeagueCurrentMatchDay": l.LeagueCurrentMatchDay,
            "LeagueLogoUrl": l.LeagueLogoUrl
        }
        leaguesdata.append(jso)
  
    return render(request,"website/leagues.html",context={"data":leaguesdata})
def clubs(request):
    teamsdata = []
    teams = DBModel.TeamsData.objects()
    for l in teams:
        jsd={
            "FaTeamName": l.FaTeamName,
            "ImageUrl": l.TeamImage,
            "LeagueName":l.League.LeagueName
        }
        teamsdata.append(jsd)
    return render(request,"website/clubs.html",context={"data":teamsdata})
@csrf_exempt 
def matches(request):
    leaguesdata = []
    leagesarr = DBModel.LeaguesData.objects()
    for l in leagesarr:
        jso={
            "id": l.id,
            "LeagueName": l.LeagueName,
            
        }
        leaguesdata.append(jso)


    matchesdata = []
    matchesarr = DBModel.MatchData.objects()
    for l in matchesarr:
        jso={
            "id": l.id,
            "HomeTeam": l.HomeTeam.FaTeamName,
            "HomeTeamImage": l.HomeTeam.TeamImage,
            "AwayTeam": l.AwayTeam.FaTeamName,
            "AwayTeamImage": l.AwayTeam.TeamImage,
            "Date": l.Date,
            "Time": l.Time,
            "League": l.League.LeagueName,
            "LeagueImage": l.League.LeagueLogoUrl,
            
        }
        matchesdata.append(jso)    
    if request.method == "POST":
        print(request.POST)   
        if "hometeam" in request.POST:
            print("in Insert")
            league = DBModel.LeaguesData.objects(id=request.POST.get("leagueid")).get()
            hometeam = DBModel.TeamsData.objects(id=request.POST.get("hometeam")).get()
            awayteam = DBModel.TeamsData.objects(id=request.POST.get("awayteam")).get()
            date = request.POST.get("date")
            time = request.POST.get("time")
            matchedata = DBModel.MatchData()
            matchedata.League = league
            matchedata.HomeTeam = hometeam
            matchedata.AwayTeam = awayteam
            matchedata.Date = date
            matchedata.Time = time
            matchedata.isActive = True
            matchedata.save()
            HttpResponse({"status":"ok"})
        if "leagueid" in request.POST:
            league = DBModel.LeaguesData.objects(id=request.POST.get("leagueid")).get()
            teams = DBModel.TeamsData.objects(League=league)
            teamsarr=[]
            for l in teams:

                jso={
                    "id":l.id,
                    "TeamName":l.FaTeamName
                }
                teamsarr.append(jso)
            
            return HttpResponse(json_util.dumps({"teams":teamsarr},True))
        
           


    return render(request,"website/matches.html",context={"leagues":leaguesdata,"matches":matchesdata})   
@csrf_exempt 
def results(request):
    if request.method == "POST":
        fields = request.POST
        print( fields)


        matchid = request.POST.get("matchid")
        homegoals = request.POST.get("homegoals")
        homeposition= request.POST.get("homeposition")
        homeyellowcard = request.POST.get("homeyellowcard")
        homeredcard = request.POST.get("homeredcard")
        homepass = request.POST.get("homepasses")
        homecorner = request.POST.get("homecorners")
        ############################################
        awaygoals = request.POST.get("awaygoals")
        awayposition= request.POST.get("awayposition")
        awayyellowcard = request.POST.get("awayyelowcard")
        awayredcard = request.POST.get("awayredcard")
        awaypass = request.POST.get("awaypasses")
        awaycorner = request.POST.get("awaycorners")
        match = DBModel.MatchData.objects(id=matchid).get()

        result = DBModel.MatchResults()
        result.Match = match
        result.HomeGoals = int(homegoals)
        result.HomePosition = int(homeposition)
        result.HomeYellowCard = int(homeyellowcard)
        result.HomeRedCarde = int(homeredcard)
        result.HomePasses = int(homepass)
        result.HomeCorners = int(homecorner)
        ###############################
        result.AwayGoals = int(awaygoals)
        result.AwayPosition = int(awayposition)
        result.AwayYellowCard = int(awayyellowcard)
        result.AwayRedCard = int(awayredcard)
        result.AwayPasses = int(awaypass)
        result.AwayCorners = int(awaycorner)
        winner = "d"
        if int(homegoals) > int(awaygoals):
            winner = "h"
        elif int(homegoals) < int(awaygoals):
            winner = "a"
        else:
            winner = "d"        
        result.WinnerTeam = winner
        result.isSet = False

        result.save()
        match.isActive = False
        match.save()
        HttpResponse( json_util.dumps({"status":"ok"},True) )
    
    matchesdata = []
    matchesarr = DBModel.MatchData.objects(isActive=True)
    for l in matchesarr:
        jso={
            "id": l.id,
            "HomeTeamName": l.HomeTeam.FaTeamName,
            "AwayTeamName": l.AwayTeam.FaTeamName,
            
            
            
        }
        matchesdata.append(jso) 
    resultdata = []
    resultarr = DBModel.MatchResults.objects()
    for h in resultarr:
        jso={
            "id": h.id,
            "HomeTeamName": h.Match.HomeTeam.FaTeamName,
            "AwayTeamName": h.Match.AwayTeam.FaTeamName,
            "HomeTeamImage": h.Match.HomeTeam.TeamImage,
            "AwayTeamImage":h.Match.AwayTeam.TeamImage,
            "MatchDate":h.Match.Date,
            "MatchTime":h.Match.Time,
            
            
        }
        resultdata.append(jso)           
    return render(request,"website/matchresults.html",context={"matches":matchesdata,"results":resultdata})      
