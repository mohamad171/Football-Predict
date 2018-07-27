from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('panel',views.panelindex,name='main'),
    path('panel/leagues',views.leagues,name='leagues'),
    path('panel/clubs',views.clubs,name='clubs'),
    path('panel/matches',views.matches,name='matches'),
    path('panel/matches/results',views.results,name='results')
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
