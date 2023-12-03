from django.urls import path
from . import views
from .views import SetPlayersView, StartGameView, GameStateView, ChallengeView, AmbassadorExchangeView, CaptainStealView, AssassinAssassinateView, DukeTaxView, IncomeView, ForeignAidView, CoupView

urlpatterns = [
    path('set_players/', SetPlayersView.as_view(), name='set-players'),
    path('start_game/', StartGameView.as_view(), name='start_game'),
    path('game_state/<int:game_id>/', GameStateView.as_view(), name='get_state'),
    path('challenge/<int:game_id>/', ChallengeView.as_view(), name='challenge'),
    # General Action
    path('income/<int:game_id>/', IncomeView.as_view(), name='income'),



    path('coup/<int:game_id>/<int:target_id>/<int:card_id>/',
         CoupView.as_view(), name='coup'),


    path('foreign_aid/<int:game_id>/',
         ForeignAidView.as_view(), name='foreign_aid'),
    path('assassinate/<int:game_id>/<int:target_id>/<int:card_id>/',
         AssassinAssassinateView.as_view(), name='assassinate'),
    # Influence Actions
    path('exchange/<int:game_id>/',
         AmbassadorExchangeView.as_view(), name='exchange'),
    path('exchange/confirm/<int:game_id>/',
         AmbassadorExchangeView.as_view(), name='confirm_exchange'),
    path('steal/<int:game_id>/<int:target_id>/',
         CaptainStealView.as_view(), name='steal'),
    path('tax/<int:game_id>/', DukeTaxView.as_view(), name='tax'),
]
