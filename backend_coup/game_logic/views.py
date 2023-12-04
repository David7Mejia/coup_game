from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .game_logic import initialize_game, start_game, get_game_state, challenge_action
from .bot_player import BotPlayer  # Import the BotPlayer class
from .models import GameState
import random
import time
import logging



# Create your views here.


class SetPlayersView(APIView):
    def post(self, request, format=None):
        num_players = request.data.get('num_players')
        start = request.data.get('start_game')

        if num_players is None or not isinstance(num_players, int):
            return Response({'error': 'Number of players not provided or invalid'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Implement this function to set up the game
            game_data = initialize_game(num_players, start)
            return Response({'message': f'Game initialized with {num_players} players', 'game_data': game_data}, status=status.HTTP_200_OK)
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


# Define available actions for bots
available_actions = ['Income', 'ForeignAid', 'Coup', 'DukeTax',
                     'AssassinAssassinate', 'CaptainSteal', 'AmbassadorExchange']

# Configure logging
logger = logging.getLogger(__name__)


class NextTurnView(APIView):
    def post(self, request, game_id):
        try:
            game_instance = GameState.objects.get(id=game_id)
            game_state = game_instance.get_game_state()

            if 'actions' not in game_state:
                game_state['actions'] = []

            def update_turn():
                new_turn = (game_state['current_turn'] +
                            1) % game_state['num_players']
                game_state['current_turn'] = new_turn
                game_instance.set_game_state(game_state)

            def record_action(player_id, action):
                game_state['actions'].append(
                    {'player_id': player_id, 'action': action})

            def process_bot_turn(bot_player_id):
                bot_player = game_state['players'][bot_player_id]
                start_time = time.time()
                available_actions = ['Income', 'ForeignAid', 'DukeTax', 'AssassinAssassinate',
                                     'CaptainSteal', 'AmbassadorExchange']  # Adjust as per your game rules
                bot_player_instance = BotPlayer(bot_player_id)
                selected_action = bot_player_instance.take_random_action(
                    available_actions)
                record_action(bot_player_id, selected_action)

                # Implement action-specific logic for bot players
                if selected_action == 'Income':
                    bot_player['coins'] += 1
                    game_state['treasury'] -= 1
                elif selected_action == 'ForeignAid':
                    bot_player['coins'] += 2
                    game_state['treasury'] -= 2
                elif selected_action == 'DukeTax':
                    bot_player['coins'] += 3
                    game_state['treasury'] -= 3
                elif selected_action == 'AssassinAssassinate':
                    # Implement logic for assassination (e.g., reduce coins, remove target card)
                    pass
                elif selected_action == 'CaptainSteal':
                    # Implement logic for stealing (e.g., transfer coins from target to bot)
                    pass
                elif selected_action == 'AmbassadorExchange':
                    # Implement logic for ambassador exchange (e.g., exchange cards)
                    pass

                # Limit bot decision to 1 second
                while time.time() - start_time < 1:
                    time.sleep(0.1)  # Sleep to avoid busy waiting

            current_player_id = game_state['current_turn']
            current_player = game_state['players'][current_player_id]

            if current_player.get('is_human'):
                human_action = request.data.get('action', 'Unknown')
                record_action(current_player_id, human_action)
                update_turn()
            else:
                process_bot_turn(current_player_id)
                update_turn()

            while True:
                next_player_id = game_state['current_turn']
                next_player = game_state['players'][next_player_id]
                if next_player.get('is_bot'):
                    process_bot_turn(next_player_id)
                    update_turn()
                else:
                    break

            return Response({'message': 'Turn processed', 'game_data': game_state})

        except GameState.DoesNotExist:
            return Response({'error': 'Game not found'}, status=status.HTTP_404_NOT_FOUND)


class ChallengeView(APIView):
    """Challenge a player's action in a game"""

    def post(self, request, game_id):
        challenger_id = request.data.get('challenger_id')
        challenged_action = request.data.get('challenged_action')

        try:
            # Retrieve the current game state
            game_instance = GameState.objects.get(id=game_id)
            game_state = game_instance.get_game_state()

            # Determine the target player based on the current game state
            target_player_id = game_state['current_action_player_id']

            # Check if there's a valid action to challenge
            if game_state['current_action'] != challenged_action:
                return Response({'error': 'No such action to challenge or action is not current'}, status=status.HTTP_400_BAD_REQUEST)

            # Proceed with the challenge
            result = challenge_action(
                game_id, challenger_id, target_player_id, challenged_action)
            return Response(result, status=status.HTTP_200_OK)

        except GameState.DoesNotExist:
            return Response({'error': 'Game not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# GENERAL ACTIONS


class IncomeView(APIView):
    def post(self, request, game_id):
        try:
            game_instance = GameState.objects.get(id=game_id)
            game_state = game_instance.get_game_state()

            # Assuming the current player is the one taking the action
            current_player_id = game_state['current_turn']
            current_player = game_state['players'][current_player_id]

            # Add 1 coin to the current player's coins
            current_player['coins'] += 1
            game_state['treasury'] -= 1
            # Update game state
            game_instance.set_game_state(game_state)
            return Response({'message': 'Income action completed', 'game_data': game_state})

        except GameState.DoesNotExist:
            return Response({'error': 'Game not found'}, status=status.HTTP_404_NOT_FOUND)


class ForeignAidView(APIView):
    def post(self, request, game_id):
        try:
            game_instance = GameState.objects.get(id=game_id)
            game_state = game_instance.get_game_state()

            # Assuming the current player is the one taking the action
            current_player_id = game_state['current_turn']
            current_player = game_state['players'][current_player_id]

            # Add 2 coins to the current player's coins
            current_player['coins'] += 2
            game_state['treasury'] -= 2
            # Update game state
            game_instance.set_game_state(game_state)
            return Response({'message': 'Foreign aid action completed', 'game_data': game_state})

        except GameState.DoesNotExist:
            return Response({'error': 'Game not found'}, status=status.HTTP_404_NOT_FOUND)


class CoupView(APIView):
    def post(self, request, game_id, target_id, card_id):
        try:
            game_instance = GameState.objects.get(id=game_id)
            game_state = game_instance.get_game_state()

            current_player_id = game_state['current_turn']
            current_player = game_state['players'][current_player_id]

            if current_player['coins'] >= 7:
                current_player['coins'] -= 7
                game_state['treasury'] += 7

                target_player = game_state['players'][target_id]

                target_player['cards'].pop(card_id)

                game_instance.set_game_state(game_state)
                return Response({'message': 'Coup action completed', 'game_data': game_state})
            else:
                return Response({'error': 'Not enough coins'}, status=status.HTTP_400_BAD_REQUEST)

        except GameState.DoesNotExist:
            return Response({'error': 'Game not found'}, status=status.HTTP_404_NOT_FOUND)

# INFLUENCE ACTIONS


class DukeTaxView(APIView):
    def post(self, request, game_id):
        try:
            game_instance = GameState.objects.get(id=game_id)
            game_state = game_instance.get_game_state()

            # Assuming the current player is the one taking the action
            current_player_id = game_state['current_turn']
            current_player = game_state['players'][current_player_id]

            # Add 3 coins to the current player's coins
            current_player['coins'] += 3
            game_state['treasury'] -= 3
            # Update game state
            game_instance.set_game_state(game_state)
            return Response({'message': 'Duke tax action completed', 'game_data': game_state})

        except GameState.DoesNotExist:
            return Response({'error': 'Game not found'}, status=status.HTTP_404_NOT_FOUND)


class AssassinAssassinateView(APIView):
    def post(self, request, game_id, target_id, card_id):
        try:
            game_instance = GameState.objects.get(id=game_id)
            game_state = game_instance.get_game_state()

            current_player_id = game_state['current_turn']
            current_player = game_state['players'][current_player_id]

            if current_player['coins'] >= 3:
                current_player['coins'] -= 3
                game_state['treasury'] += 3

                target_player = game_state['players'][target_id]

                target_player['cards'].pop(card_id)

                game_instance.set_game_state(game_state)
                return Response({'message': 'Assassination attempt made', 'game_data': game_state})
            else:
                return Response({'error': 'Not enough coins'}, status=status.HTTP_400_BAD_REQUEST)

        except GameState.DoesNotExist:
            return Response({'error': 'Game not found'}, status=status.HTTP_404_NOT_FOUND)


class CaptainStealView(APIView):
    def post(self, request, game_id, target_id):
        try:
            game_instance = GameState.objects.get(id=game_id)
            game_state = game_instance.get_game_state()

            current_player_id = game_state['current_turn']
            current_player = game_state['players'][current_player_id]
            target_player = game_state['players'][target_id]

            steal_amount = 2
            target_player['coins'] -= steal_amount
            current_player['coins'] += steal_amount

            game_instance.set_game_state(game_state)
            return Response({'message': f'Stolen {steal_amount} coins', 'game_data': game_state})

        except GameState.DoesNotExist:
            return Response({'error': 'Game not found'}, status=status.HTTP_404_NOT_FOUND)


class AmbassadorExchangeView(APIView):
    def post(self, request, game_id):
        try:
            game_instance = GameState.objects.get(id=game_id)
            game_state = game_instance.get_game_state()

            current_player_id = game_state['current_turn']
            current_player = game_state['players'][current_player_id]

            # Simulate drawing 2 random cards from the Court deck
            court_deck = game_state['deck_card_counts']
            # Convert dictionary keys to a list
            court_deck_keys = list(court_deck.keys())
            # Shuffle the list of keys
            random.shuffle(court_deck_keys)

            # Take 2 random cards temporarily
            temporary_cards = court_deck_keys[:2]

            # Update game state to reflect temporary cards for the current player
            current_player['temporary_cards'] = temporary_cards

            game_state['game_id'] = game_id
            game_instance.set_game_state(game_state)
            return Response({'message': 'Temporary cards drawn', 'temporary_cards': temporary_cards})

        except GameState.DoesNotExist:
            return Response({'error': 'Game not found'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, game_id):
        try:
            game_instance = GameState.objects.get(id=game_id)
            game_state = game_instance.get_game_state()

            current_player_id = game_state['current_turn']
            current_player = game_state['players'][current_player_id]

            selected_card_for_exchange_ids = request.data.get(
                'selected_card_for_exchange', [])
            selected_temporary_cards_types = request.data.get(
                'selected_temporary_cards', [])

            # Perform the card exchange
            new_cards = []
            for card in current_player['cards']:
                if card.get('id') in selected_card_for_exchange_ids:
                    # Replace with temporary cards
                    for card_type in selected_temporary_cards_types:
                        # Reuse the same ID or generate a new one
                        new_card = {'type': card_type, 'id': card['id']}
                        new_cards.append(new_card)
                else:
                    new_cards.append(card)

            current_player['cards'] = new_cards

            game_state['game_id'] = game_id
            game_instance.set_game_state(game_state)

            return Response({'message': 'Exchange completed', 'new_cards': selected_temporary_cards_types, 'updated_player_cards': current_player['cards'], 'game_data': game_state})

        except GameState.DoesNotExist:
            return Response({'error': 'Game not found'}, status=status.HTTP_404_NOT_FOUND)
