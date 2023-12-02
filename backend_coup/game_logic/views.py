from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .game_logic import initialize_game, start_game, get_game_state

# Create your views here.

class SetPlayersView(APIView):
    def post(self, request, format=None):
        num_players = request.data.get('num_players')

        if num_players is None or not isinstance(num_players, int):
            return Response({'error': 'Number of players not provided or invalid'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            game_state = initialize_game(num_players)  # Implement this function to set up the game
            return Response({'message': f'Game initialized with {num_players} players', 'game_state': game_state}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class StartGameView(APIView):
    def post(self, request, format=None):
        start = request.data.get('start_game')

        if start is None or not isinstance(start, bool):
            return Response({'error': 'Start game is not provided or invalid'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            game_state = start_game(start)
            return Response({'message': f'Let\'s Game!', 'game_state': game_state}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class GameStateView(APIView):
    def get(self, request, *args, **kwargs):
        game_id = kwargs.get('game_id')
        if game_id is None:
            return Response({"error": "Game ID is missing."}, status=status.HTTP_400_BAD_REQUEST)

        game_state = get_game_state(game_id)
        if game_state is not None:
            return Response(game_state)
        else:
            return Response({"error": "Game not found."}, status=status.HTTP_404_NOT_FOUND)

