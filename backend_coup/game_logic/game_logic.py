import random
from django.db import transaction
from .models import GameState
from django.core import serializers
from rest_framework.response import Response
from rest_framework import status
from .bot_player import BotPlayer  # Import the BotPlayer class
from .models import GameState  # Ensure this is imported


import random
from django.db import transaction


@transaction.atomic
def initialize_game(num_players, start):
    print(num_players, 'Initializing game...')

    if num_players < 3:
        raise ValueError("At least 3 players are required to start the game.")
    if num_players > 6:
        raise ValueError("The maximum number of players allowed is 6.")

    initial_card_counts = {'Duke': 3, 'Assassin': 3,
                           'Captain': 3, 'Ambassador': 3, 'Contessa': 3}
    players = []

    for player_id in range(num_players):
        player = {
            'id': player_id,
            'name': f'Player {player_id + 1}',
            'coins': 2,
            'cards': [],
            'is_human': player_id == 0,  # First player is human, rest are bots
            'is_bot': player_id != 0,    # Indicates if the player is a bot
        }
        players.append(player)

    # Calculate the total number of coins available in the pile
    total_coins = 50 - (num_players * 2)

    # Initialize the game state
    game_state = {
        'num_players': num_players,
        'players': players,
        'current_turn': 0,
        'game_status': 'started',
        'treasury': total_coins,
        'deck_card_counts': initial_card_counts.copy(),
    }

    # Create and shuffle a deck of character cards
    deck = [{'id': i + 1, 'type': card_type} for i, card_type in enumerate(
        sum(([card] * count for card, count in initial_card_counts.items()), []))]
    random.shuffle(deck)

    # Distribute cards to each player sequentially
    for i in range(num_players):
        for j in range(2):
            card_index = i * 2 + j
            if card_index < len(deck):
                players[i]['cards'].append(deck[card_index])
                game_state['deck_card_counts'][deck[card_index]['type']] -= 1

    # Save the game state to the database
    game_instance = GameState.objects.create(**game_state)
    game_state['game_id'] = game_instance.id

    return game_state



# @transaction.atomic
# def initialize_game(num_players, start):
#     print(num_players, 'Initializing game...')

#     if num_players < 3:
#         raise ValueError("At least 3 players are required to start the game.")
#     if num_players > 6:
#         raise ValueError("The maximum number of players allowed is 6.")

#     initial_card_counts = {'Duke': 3, 'Assassin': 3,
#                            'Captain': 3, 'Ambassador': 3, 'Contessa': 3}

#     players = []

#     for player_id in range(num_players):
#         player = {
#             'id': player_id,
#             'name': f'Player {player_id + 1}',
#             'coins': 2,
#             'cards': [],
#             'is_human': player_id == 0,  # First player is human, rest are bots
#         }
#         players.append(player)

#     # Calculate the total number of coins available in the pile
#     total_coins = 50 - (num_players * 2)

#     # Initialize the game state
#     game_state = {
#         'num_players': num_players,
#         'players': players,
#         'current_turn': 0,
#         'game_status': 'started',
#         'treasury': total_coins,
#         'deck_card_counts': initial_card_counts.copy(),
#     }

#     # Create and shuffle a deck of character cards with unique numerical IDs
#     deck = [{'id': i + 1, 'type': card_type} for i, card_type in enumerate(
#         sum(([card] * count for card, count in initial_card_counts.items()), []))]
#     random.shuffle(deck)

#     # Distribute cards to each player sequentially
#     for i in range(num_players):
#         for j in range(2):
#             card_index = i * 2 + j
#             if card_index < len(deck):
#                 players[i]['cards'].append(deck[card_index])
#                 game_state['deck_card_counts'][deck[card_index]['type']] -= 1

#     game_instance = GameState.objects.create(**game_state)
#     game_state['game_id'] = game_instance.id

#     return game_state


@transaction.atomic
def update_game(game_id, new_state):
    try:
        game_instance = GameState.objects.get(id=game_id)
        game_instance.set_game_state(new_state)
    except GameState.DoesNotExist:
        raise ValueError(f"Game with ID {game_id} does not exist.")


@transaction.atomic
def start_game(game_id, start):
    try:
        game_instance = GameState.objects.get(id=game_id)
        game_state = game_instance.get_game_state()

        # Update the game state
        game_state['game_status'] = 'started' if start else 'not_started'

        # Save the updated state back to the database
        game_instance.set_game_state(game_state)
    except GameState.DoesNotExist:
        raise ValueError("Game with provided ID does not exist.")


def get_game_state(game_id):
    try:
        game_instance = GameState.objects.get(id=game_id)
        return game_instance.get_game_state()
    except GameState.DoesNotExist:
        return None


@transaction.atomic
def challenge_action(game_id, challenger_id, target_player_id, challenged_action):
    game_instance = GameState.objects.get(id=game_id)
    game_state = game_instance.get_game_state()

    # Check if the challenge is valid (e.g., correct timing, action is challengeable)
    # This will depend on your game's rules
    # complete this function

    # - Determine if the challenged player was bluffing
    # - Apply consequences based on the outcome
    # Example outcome handling (modify according to your game's rules):
    if bluff_detected:
        # Penalize the bluffing player
        pass
    else:
        pass
        # Penalize the challenger

    # Update the game state
    game_instance.set_game_state(game_state)

    # Return the updated game state or a result indication
    return game_state
