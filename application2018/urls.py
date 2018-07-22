from django.urls import path

from . import views

urlpatterns = [
    path('getleagues',views.leaguetable,name='leagutable'),

]