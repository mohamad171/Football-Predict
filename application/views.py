from django.shortcuts import render
from pymongo import MongoClient
import json
from . import predict
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.template import loader
from . import jalali
import datetime  
from footballpredict.beakerfile import cache
from worldcup import WorldCupClass
from django.views.decorators.http import require_http_methods


worlcup = WorldCupClass.WorlCup()



# Create your views here.
client = MongoClient("mongodb://localhost:8085/")

footpredict = predict.FootballPredict("224adf37e96d48568b30d24ece1d474a")
leaguearr = ['PL','PD','BL1','SA','FL1','DED']
@require_http_methods(["POST"])
@csrf_exempt
def main(request):
        template = loader.get_template("application/main.xml")
        return HttpResponse(template.render())  
@require_http_methods(["POST"])
@csrf_exempt
def leaguetable(request,leaguename):
    matcharr = worlcup.GetGroupTable("Group "+leaguename)
    template = loader.get_template("application/leaguetable.xml")    
    context =     {"status":"ok","data":matcharr}
    return HttpResponse(template.render(context))
#   if request.method == "POST":
#     if leaguename in leaguearr:
#         @cache.region('short_term')
#         def getdata():
#             arr = []
#             tableurl = client.footballpredict.leagues.find_one({"league":leaguename})
#             data = footpredict.SendRequest(tableurl["leaguetable"])
#             for l in data["standing"]:
#                 teamdata = client.footballpredict.teams.find_one({"teamname":l["teamName"]})
#                 if teamdata != None:
#                     imageurl = teamdata["imageurl"]
#                 else:
#                     imageurl = "null"
#                 outputdata = {
#             "position": l["position"],
#             "teamName": teamdata["fateamname"],
#             "points": l["points"],
#             "playedGames": l["playedGames"],
#             "imageurl": imageurl
#                 }
#                 arr.append(outputdata)
#             return arr
#         result = getdata()      
#         template = loader.get_template("application/leaguetable.xml")    
#         context =     {"status":"ok","data":result}
#         return HttpResponse(template.render(context))
#     else:
#         return HttpResponse("League Not Found")
#   else:
#        return HttpResponse("Invalid Request Method")
@require_http_methods(["POST"])
@csrf_exempt                    
def nowfixures(request , leaguename):
#    if request.method == "POST":
#     if leaguename in leaguearr:
#        @cache.region('short_term')
#        def getdata(): 
#         arr = []
#         leaguedata = client.footballpredict.leagues.find_one({"league":leaguename})
        
#         if "nowmatches" in leaguedata:
#             for l in leaguedata["nowmatches"]:
#                 hour = int(l["date"].split("T")[1].split(":")[0])
#                 minute = int(l["date"].split("T")[1].split(":")[1])
#                 ftime = datetime.datetime(1998,1,1,hour,minute)
#                 finaltime = ftime + datetime.timedelta(hours=4,minutes=30)
#                 outputdata = {
#                 "datetime": jalali.Gregorian(l["date"].split("T")[0]).persian_string() + " " + str(finaltime.hour) + ":" + str(finaltime.minute),
#                 "hometeamname": l["homeTeamName"],
#                 "awayteamname": l["awayTeamName"]
#         }
#                 arr.append(outputdata)
#         return arr

       template = loader.get_template("application/nowfixures.xml") 
       result = matcharr , videoarr = worlcup.GetMainData("Group "+leaguename)         
       context =  {"status":"ok","nowmatches":matcharr}      
       return HttpResponse(template.render(context))
#     else:
#         return HttpResponse("League Not Found")    
#    else:
#        return HttpResponse("Not Allowed Method") 

@require_http_methods(["POST"])
@csrf_exempt             
def nextfixures(request , leaguename):
   if request.method == "POST": 
    if leaguename in leaguearr:
       @cache.region('short_term')
       def getdata(): 
        arr = []
        leaguedata = client.footballpredict.leagues.find_one({"league":leaguename})
        
        if "nextmatches" in leaguedata:
            for l in leaguedata["nextmatches"]:
                hour = int(l["date"].split("T")[1].split(":")[0])
                minute = int(l["date"].split("T")[1].split(":")[1])
                ftime = datetime.datetime(1998,1,1,hour,minute)
                finaltime = ftime + datetime.timedelta(hours=4,minutes=30)
                outputdata = {
                "datetime": jalali.Gregorian(l["date"].split("T")[0]).persian_string() + " " + str(finaltime.hour) + ":" + str(finaltime.minute),
                "hometeamname": l["homeTeamName"],
                "awayteamname": l["awayTeamName"]
        }
                arr.append(outputdata)
            return arr
            
       template = loader.get_template("application/nextfixures.xml") 
       result = getdata()
       context =  {"status":"ok","nextmatches":result}      
       return HttpResponse(template.render(context))
    else:
        return HttpResponse("League Not Found")     
   else:
       return HttpResponse("Not Allowed Method")        
