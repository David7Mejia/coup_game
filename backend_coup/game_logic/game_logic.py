import random
from django.db import transaction
from .models import GameState

@transaction.atomic
def initialize_game(num_players):
    print(num_players, 'asdsadsdadasdadsasd')
    if num_players < 3:
        raise ValueError("At least 3 players are required to start the game.")

    if num_players > 6:
        raise ValueError("The maximum number of players allowed is 6.")

    # Define the character card types and quantities
    initial_card_counts = {'Duke': 3, 'Assassin': 3, 'Captain': 3, 'Ambassador': 3, 'Contessa': 3}

    # Create player objects
    players = []
    for player_id in range(num_players):
        player = {
            'id': player_id,
            'name': f'Player {player_id + 1}',  # Assign default names
            'coins': 2,  # Give each player 2 coins at the beginning
            'cards': [],  # Initialize empty hand for each player
        }
        players.append(player)

    # Calculate the total number of coins available in the pile
    total_coins = 50 - (num_players * 2)  # 2 coins per player

    # Initialize the game state
    game_state = {
        'num_players': num_players,
        'players': players,
        'current_turn': 0,  # Initialize the turn to the first player
        'game_status': 'not_started',
        'treasury': total_coins,  # Track the total coins available
        'deck_card_counts': initial_card_counts.copy(),  # Track card counts
    }

    # Create a deck of character cards based on initial quantities
    deck = []
    for card, count in initial_card_counts.items():
        deck.extend([card] * count)

    # Shuffle the deck to randomize card distribution
    random.shuffle(deck)

    # Deal 2 cards to each player, keeping the distribution hidden
    for player in players:
        for _ in range(2):
            card = deck.pop()  # Take a card from the top of the shuffled deck
            player['cards'].append(card)  # Add the card to the player's hand
            # Decrement the card count in game state
            game_state['deck_card_counts'][card] -= 1

    # Return the initialized game state

    game_instance = GameState.objects.create(**game_state)
    return game_instance.id

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
    game_instance
