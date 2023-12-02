from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .game_logic import initialize_game

# Create your views here.

class SetPlayersView(APIView):
    def post(self, request, format=None):
        num_players = request.data.get('num_players')

        if num_players is None or not isinstance(num_players, int):
            return Response({'error': 'Number of players not provided or invalid'}, status=status.HTTP_400_BAD_REQUEST)

        # Here, you can add logic to initiate the game with the specified number of players
        # For example, creating Player objects and adding them to the game state
        # Make sure to handle cases where the number of players is not feasible
        # ...

        try:
            game_state = initialize_game(num_players)  # Implement this function to set up the game
            return Response({'message': f'Game initialized with {num_players} players', 'game_state': game_state}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

