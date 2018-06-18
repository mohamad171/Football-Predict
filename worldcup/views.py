from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from . import DBModel
from django.views.decorators.http import require_http_methods
import json
import pprint
import bson
import requests
from . import WorldCupClass

worlcup = WorldCupClass.WorlCup()


@csrf_exempt
@require_http_methods(["GET"])
def GetCSVFile(request):
    response = requests.get("http://www.vpngate.net/api/iphone/")
    return HttpResponse(response.text)

@csrf_exempt
@require_http_methods(["POST"])
def GetUserData(request):
    # {"BannerImage":"http://static1.tamasha.com/files/pictures/thumb/01307410.jpg"},{"BannerImage":"http://static1.tamasha.com/files/pictures/thumb/01307410.jpg"},{"BannerImage":"http://static1.tamasha.com/files/pictures/thumb/01307410.jpg"},{"BannerImage":"http://static1.tamasha.com/files/pictures/thumb/01307410.jpg"}
    bannerarr = []
    deviceid = request.POST.get("deviceid")
    return HttpResponse(json.dumps({"status":"ok","section":"group","section_text":"groupSec","section_tag":"group","bannerarr":bannerarr}))


@csrf_exempt
@require_http_methods(["POST"])
def SetUpMatchResult(request):
    matchid = request.POST.get("matchid")
    homegoals = request.POST.get("homegoals")
    awaygoals = request.POST.get("awaygoals")
    matchdata = DBModel.MatchData.objects(id=matchid).get()
    result = worlcup.SetMatchResult(matchdata,homegoals,awaygoals)

    if result == "ok":
        res = worlcup.SetGroupTable(matchdata)
        if res == "ok":
            return HttpResponse(json.dumps({"status":"ok"}))
        else:
            return HttpResponse(json.dumps({"status":"faild"}))

    else:
        return HttpResponse(json.dumps({"status":"faild"}))




@csrf_exempt
@require_http_methods(["POST"])
def GetMainData(request):
    # matchid = "5b082752ace15721c0313167"
    # matchdata = DBModel.MatchData.objects(id=matchid).get()
    # results = DBModel.MatchResults()
    # results.Match = matchdata
    # results.HomeGoals = 2
    # results.AwayGoals = 3
    # results.save()

    # Add Group To Teams Data
    # SetMatchResult(matchdata,4,3)
    #SetGroupTable(matchdata)
    # SetVideo(matchdata,"http://","نمونه")
    # 
    groupname = request.POST.get("group")
    matcharr , videoarr = worlcup.GetMainData(groupname)
    return HttpResponse( json.dumps({"status":"ok","matchdata":matcharr,"videodata":videoarr} ) )
@csrf_exempt
@require_http_methods(["POST"])
def GetLeagueTable(request):
    groupname = request.POST.get("group")
    teamsarr = worlcup.GetGroupTable(groupname)
    return HttpResponse( json.dumps({"status":"ok","teamsdata":teamsarr} ) )    