import random
import time
import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .game_logic import initialize_game, start_game, get_game_state, challenge_action
from .bot_player import BotPlayer  # Import the BotPlayer class
from .models import GameState
# from .utils import record_action  # Import the shared function


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

    def check_for_game_end(self, game_state):
        active_players = [p for p in game_state['players']
                          if not p.get('is_eliminated', False)]
        if len(active_players) == 1:
            game_state['game_status'] = 'ended'
            game_state['winner'] = active_players[0]['id']
            game_instance.set_game_state(game_state)
            return True
        return False

    def post(self, request, game_id):
        try:
            game_instance = GameState.objects.get(id=game_id)
            game_state = game_instance.get_game_state()

            if 'actions' not in game_state:
                game_state['actions'] = []

            def update_turn():
                original_turn = game_state['current_turn']
                new_turn = (original_turn + 1) % game_state['num_players']

                # Loop to find the next non-eliminated player
                while game_state['players'][new_turn].get('is_eliminated', False):
                    new_turn = (new_turn + 1) % game_state['num_players']
                    # Break the loop if we've checked all players and are back at the original turn
                    if new_turn == original_turn:
                        break

                game_state['current_turn'] = new_turn
                game_instance.set_game_state(game_state)

            def record_action(player_id, action):
                game_state['actions'].append(
                    {'player_id': player_id, 'action': action})

            def process_bot_turn(bot_player_id):
                bot_player = game_state['players'][bot_player_id]
                # Check if the bot player is eliminated
                if bot_player.get('is_eliminated', False):
                    return  # Skip turn if player is eliminated
                start_time = time.time()
                available_actions = ['Income', 'ForeignAid', 'DukeTax',
                                     'CaptainSteal', 'AmbassadorExchange']  # Adjust as per your game rules
                if bot_player['coins'] >= 3:
                    available_actions.append('AssassinAssassinate')
                bot_player_instance = BotPlayer(bot_player_id)
                selected_action = bot_player_instance.take_random_action(
                    available_actions)
                # record_action(bot_player_id, selected_action)

                # Implement action-specific logic for bot players
                if selected_action == 'Income':
                    bot_player['coins'] += 1
                    game_state['treasury'] -= 1
                    record_action(
                        bot_player_id, f'{bot_player["name"]} Gained 1 coin from Income')

                elif selected_action == 'ForeignAid':
                    bot_player['coins'] += 2
                    game_state['treasury'] -= 2
                    record_action(
                        bot_player_id, F'{bot_player["name"]} Gained 2 coins from Foreign Aid')

                elif selected_action == 'DukeTax':
                    bot_player['coins'] += 3
                    game_state['treasury'] -= 3
                    record_action(
                        bot_player_id, f'{bot_player["name"]} Gained 3 coins from Duke Tax')

                # elif selected_action == 'AssassinAssassinate':
                #     # Example assassination logic with target details
                #     target_id = random.choice(
                #         [p['id'] for p in game_state['players'] if p['id'] != bot_player_id and not p.get('is_eliminated', False)])
                #     target_player = game_state['players'][target_id]
                #     if len(target_player['cards']) > 0:
                #         card_id = random.choice(
                #             range(len(target_player['cards'])))
                #         del target_player['cards'][card_id]
                #         if len(target_player['cards']) == 0:
                #             target_player['is_eliminated'] = True
                #         record_action(
                #             bot_player_id, f'{bot_player["name"]} Assassinated a card of Player {target_id + 1}')

                # elif selected_action == 'CaptainSteal':
                #     # Example stealing logic with target details
                #     target_id = random.choice(
                #         [p['id'] for p in game_state['players'] if p['id'] != bot_player_id and not p.get('is_eliminated', False)])
                #     target_player = game_state['players'][target_id]
                #     steal_amount = 2
                #     target_player['coins'] -= steal_amount
                #     bot_player['coins'] += steal_amount
                #     record_action(
                #         bot_player_id, f'{bot_player["name"]} Stole 2 coins from Player {target_id + 1}')
                elif selected_action == 'AssassinAssassinate':
                    eligible_targets = [p['id'] for p in game_state['players']
                                        if p['id'] != bot_player_id and not p.get('is_eliminated', False)]
                    if eligible_targets:
                        target_id = random.choice(eligible_targets)
                        target_player = game_state['players'][target_id]
                        if len(target_player['cards']) > 0:
                            card_id = random.choice(
                                range(len(target_player['cards'])))
                            del target_player['cards'][card_id]
                            if len(target_player['cards']) == 0:
                                target_player['is_eliminated'] = True
                            record_action(
                                bot_player_id, f'{bot_player["name"]} Assassinated a card of Player {target_id + 1}')
                    else:
                        pass
                        # Handle the case when there are no eligible targets

                elif selected_action == 'CaptainSteal':
                    eligible_targets = [p['id'] for p in game_state['players']
                                        if p['id'] != bot_player_id and not p.get('is_eliminated', False)]
                    if eligible_targets:
                        target_id = random.choice(eligible_targets)
                        target_player = game_state['players'][target_id]
                        steal_amount = 2
                        if target_player['coins'] >= steal_amount:
                            target_player['coins'] -= steal_amount
                            bot_player['coins'] += steal_amount
                            record_action(
                                bot_player_id, f'{bot_player["name"]} Stole 2 coins from Player {target_id + 1}')
                        else:
                            pass
                            # Handle the case when the target doesn't have enough coins to steal
                    else:
                        pass
                        # Handle the case when there are no eligible targets
                elif selected_action == 'AmbassadorExchange':
                    # Draw 2 random cards from the deck
                    court_deck_keys = list(
                        game_state['deck_card_counts'].keys())
                    random.shuffle(court_deck_keys)
                    temporary_cards = court_deck_keys[:2]

                # Select cards to exchange, ensuring we do not exceed the number of cards the bot has
                    num_cards_to_exchange = min(
                        len(temporary_cards), len(bot_player['cards']))
                    if num_cards_to_exchange > 0:
                        cards_to_exchange_indices = random.sample(
                            range(len(bot_player['cards'])), num_cards_to_exchange)
                        for index in sorted(cards_to_exchange_indices, reverse=True):
                            del bot_player['cards'][index]

                        # Add new cards
                        for card_type in temporary_cards:
                            bot_player['cards'].append(
                                {'type': card_type})  # New card without ID

                        # Record the exchange action
                        record_action(
                            bot_player_id, f'{bot_player["name"]} Exchanged {num_cards_to_exchange} cards')

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
                if not current_player.get('is_eliminated', False):
                    process_bot_turn(current_player_id)
                update_turn()
              # Check for game end after each turn
            if self.check_for_game_end(game_state):
                game_instance.set_game_state(
                    game_state)  # Save updated game state
                return Response({'message': 'Game ended', 'winner': game_state['winner'], 'game_data': game_state})

            while True:
                next_player_id = game_state['current_turn']
                next_player = game_state['players'][next_player_id]
                if next_player.get('is_bot') and not next_player.get('is_eliminated', False):
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

            # Record the action
            # record_action(game_id, current_player_id, action_description)

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

            # Record the action
            # record_action(game_id, current_player_id, action_description)

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

            # Record the action
            # record_action(game_id, current_player_id, action_description)

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

                # Remove the specified card from the target player
                del target_player['cards'][card_id]

                # Check if the target player has lost all their cards
                if len(target_player['cards']) == 0:
                    # Mark the player as eliminated
                    target_player['is_eliminated'] = True

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

            # Record the action
            # record_action(game_id, current_player_id, action_description)

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

            # Record the action

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


class RestartGameView(APIView):
    def post(self, request):
        try:
            # Assuming there's only one game instance
            game_instance = GameState.objects.first()
            if not game_instance:
                return Response({'error': 'Game instance not found'}, status=status.HTTP_404_NOT_FOUND)

            # Call initialize_game to reset the game state
            num_players = game_instance.get_game_state().get(
                'num_players', 3)  # Default to 3 players if not specified
            new_game_state = initialize_game(
                num_players, start=True)  # Adjust parameters as needed

            # Save the new game state
            game_instance.set_game_state(new_game_state)

            return Response({'message': 'Game restarted', 'game_data': new_game_state})

        except GameState.DoesNotExist:
            return Response({'error': 'Game not found'}, status=status.HTTP_404_NOT_FOUND)
