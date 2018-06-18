from django.urls import path

from . import views

urlpatterns = [
    # path('leaguetable',views.leaguetable,name='leagutable'),
    path('/maindata',views.GetMainData,name='GetMainData'),
    path('/grouptable',views.GetLeagueTable,name='GetLeagueTable'),
    path('/setmatchresult',views.SetUpMatchResult,name='SetUpMatchResult'),
    path('/getdata',views.GetCSVFile,name='GetCSVFile'),
    path('/getuserdata',views.GetUserData,name='GetCSVFile'),
    # path('<leaguename>/matchvideos',views.nextfixures,name='matchvideos'),
    # path('<matchid>/videos',views.nextfixures,name='videos'),
    # path('',views.main,name='main')
]