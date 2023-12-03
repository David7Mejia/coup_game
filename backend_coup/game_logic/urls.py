from django.urls import path
from . import views
from .views import SetPlayersView, StartGameView, GameStateView, ChallengeView, AmbassadorExchangeView, CaptainStealView, AssassinAssassinateView, DukeTaxView

urlpatterns = [
    path('set_players/', SetPlayersView.as_view(), name='set-players'),
    path('start_game/', StartGameView.as_view(), name='start_game'),
    path('game_state/<int:game_id>/', GameStateView.as_view(), name='get_state'),
    path('challenge/<int:game_id>/', ChallengeView.as_view(), name='challenge'),
    path('assassinate/<int:game_id>/',
         AssassinAssassinateView.as_view(), name='start_game'),
    path('exchange/<int:game_id>/',
         AmbassadorExchangeView.as_view(), name='start_game'),
    path('exchange/confirm/<int:game_id>/',
         AmbassadorExchangeView.as_view(), name='confirm_exchange'),
    path('steal/<int:game_id>/<int:target_id>',
         CaptainStealView.as_view(), name='start_game'),
    path('tax/<int:game_id>/', DukeTaxView.as_view(), name='tax'),
]
