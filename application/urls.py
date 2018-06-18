from django.urls import path

from . import views

urlpatterns = [
    path('ins/<leaguename>/leaguetable/',views.leaguetable,name='leagutable'),
    path('ins/<leaguename>/nowmatches/',views.nowfixures,name='nowfixures'),
    path('ins/<leaguename>/nextmatches/',views.nextfixures,name='nowfixures'),
    path('ins/',views.main,name='main')
]