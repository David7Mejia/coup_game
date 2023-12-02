from django.urls import path
from . import views
from .views import SetPlayersView, StartGameView,GameStateView

urlpatterns = [
    path('set_players/', SetPlayersView.as_view(), name='set-players'),
    path('start_game/', StartGameView.as_view(), name='start_game'),
    path('game_state/<int:game_id>/', GameStateView.as_view(), name='get_state')
]
