from django.urls import path
from . import views
from .views import SetPlayersView

urlpatterns = [
    path('set_players/', SetPlayersView.as_view(), name='set-players'),
]
