import requests
from pymongo import MongoClient
import json

class FootballPredict:
    __apikey = ""
    __client = MongoClient("mongodb://localhost:27017/")
    def __init__(self,api):
        self.__apikey = api
    def Predict(self,league,hometeam,awayteam,fixureurl):
        homescore = 0
        awayscore = 0
        drawscore = 0
        result = self.__calcTable(league,hometeam,awayteam)
        if result == "home":
            homescore += 10
        elif result == "away":
            awayscore += 10
        else:
            print("Team or League Not Found")
        result = self.__calcHome(league,hometeam,awayteam)
        if result == "home":
            homescore += 5
        elif result == "away":
            awayscore += 5
        elif result == "draw":
             awayscore += 2.5
             homescore += 2.5   
        else:
            print("Team or League Not Found")
        result = self.__calcGoals(league,hometeam,awayteam)
        if result == "home":
            homescore += 6
        elif result == "away":
            awayscore += 6
        elif result == "draw":
             awayscore += 3
             homescore += 3   
        else:
            print("Team or League Not Found")
        homesc , drawsc , awaysc = self.__calcHead2Head(fixureurl)   
        homescore += homesc * 2
        drawscore += drawsc * 2
        awayscore += awaysc * 2

        homewsc , homedsc , homelsc , awaywsc , awaydsc , awaylsc = self.__calcWinLossDraw(league,hometeam,awayteam)
        homescore += homewsc
        awayscore += awaywsc

        drawscore +=  round((awaydsc + homedsc) / 2)

        sumavg = homescore + drawscore + awayscore           
        print(awayteam +": " + str(self.percentage(awayscore,sumavg)) + "  ::::  " + hometeam +": " + str(self.percentage(homescore,sumavg)) + "  ::::  " + str(self.percentage(drawscore,sumavg)))    
        
    def __calcHead2Head(self,fixureurl):
        data = self.SendRequest(fixureurl)
        homewin = 0
        awaywin = 0
        draw = 0
        Head2Head = data["head2head"]
        homewin = Head2Head["homeTeamWins"]
        awaywin = Head2Head["awayTeamWins"]
        draw = Head2Head["draws"]
        return homewin , draw , awaywin
    def __calcWinLossDraw(self,league,hometeam,awayteam):
      home = self.__client.footballpredict.teams.find_one({"teamname":hometeam , "league":league})
      away = self.__client.footballpredict.teams.find_one({"teamname":awayteam , "league":league})
      if home != None and away != None:
          data = self.SendRequest("http://api.football-data.org/v1/competitions/445/leagueTable")
          for l in data["standing"]:
              if l["teamName"] == hometeam:
                  homewin = l["wins"]
                  homeloss = l["losses"]
                  homedraw = l["draws"]
              if l["teamName"] == awayteam:
                  awaywin = l["wins"]
                  awayloss = l["losses"]
                  awaydraw = l["draws"]
          return homewin , homedraw , homeloss , awaywin , awaydraw , awayloss        

      else:
          return "faild"    
    def __calcGoals(self,league,hometeam,awayteam):
      home = self.__client.footballpredict.teams.find_one({"teamname":hometeam , "league":league})
      away = self.__client.footballpredict.teams.find_one({"teamname":awayteam , "league":league})
      if home != None and away != None:
          data = self.SendRequest("http://api.football-data.org/v1/competitions/445/leagueTable")
          homegoals = 0 
          awaygoals = 0
          for l in data["standing"]:
              if l["teamName"] == hometeam:
                  homegoals = l["goalDifference"]
              if l["teamName"] == awayteam:
                  awaygoals = l["goalDifference"]
          if homegoals > awaygoals:
              return "home"
          elif awaygoals > homegoals:
              return "away"
          elif awaygoals == homegoals:
              return "draw"                     
      else:
           return "faild" 
    def __calcTable(self,league,hometeam,awayteam):
      home = self.__client.footballpredict.teams.find_one({"teamname":hometeam , "league":league})
      away = self.__client.footballpredict.teams.find_one({"teamname":awayteam , "league":league})
      if home != None and away != None:  
        homepos = 404
        awaypos = 404
        data = self.SendRequest("http://api.football-data.org/v1/competitions/445/leagueTable")
         
        for l in data["standing"]:
            if l["teamName"] == hometeam:
                homepos = l["position"]
            if l["teamName"] == awayteam:
                awaypos = l["position"]
        if hometeam > awayteam:
            return "home"
        else:
            return "away"
      else:
           return "faild"
    def __calcHome(self,league,hometeam,awayteam):
        # Calculate With Home or Away Wins
      home = self.__client.footballpredict.teams.find_one({"teamname":hometeam , "league":league})
      away = self.__client.footballpredict.teams.find_one({"teamname":awayteam , "league":league})
      if home != None and away != None:
          data = self.SendRequest("http://api.football-data.org/v1/competitions/445/leagueTable")
          homewins = 0 
          awaywins = 0
          for l in data["standing"]:
              if l["teamName"] == hometeam:
                  homewins = l["home"]["wins"]
              if l["teamName"] == awayteam:
                  awaywins = l["away"]["wins"]
          if homewins > awaywins:
              return "home"
          elif awaywins > homewins:
              return "away"
          else:
              return "draw"           
      else:
          return "faild"            
    def SendRequest(self,url):
        header = {
            "X-Auth-Token":self.__apikey
        }

        reponse = requests.get(url,headers=header)
        data = json.loads(reponse.text)
        return data
    def percentage(self,value, total, multiply=True):
	    if not isinstance(value, (int,float)):
		    return ValueError('Input values should be a number, your first input is a %s' % type(value))
	    if not isinstance(total, (int,float)):
		    return ValueError('Input values should be a number, your second input is a %s' % type(total))
	    try:
		    percent = (value / float(total))
		    if multiply:
			    percent = percent * 100
		    return round(percent,1)
	    except ZeroDivisionError:
		    return None    
        
class FootballData:
    __apikey = ""
    def __init__(self,apikey):
        self.__apikey = apikey

    def __SendRequest(self,url):
        header = {
            "X-Auth-Token" : self.__apikey
        }
        response = requests.get(url,headers=header)
        data = json.loads(response.texts)
        return data
    def __Head2Head(self,fixureurl,hometeam,awayteam):
        data = self.__SendRequest(fixureurl)
        homewin = 0
        awaywin = 0
        draw = 0
        Head2Head = data["head2head"]
        homewin = Head2Head["homeTeamWins"]
        awaywin = Head2Head["awayTeamWins"]
        draw = Head2Head["draws"]
        return homewin , draw , awaywin
            
            
    