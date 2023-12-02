import random

def initialize_game(num_players):
    if num_players < 2:
        raise ValueError("At least 2 players are required to start the game.")

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
        'players': players,
        'current_turn': 0,  # Initialize the turn to the first player
        'game_status': 'not_started',
        'total_coins_in_pile': total_coins,  # Track the total coins available
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
    return game_state
