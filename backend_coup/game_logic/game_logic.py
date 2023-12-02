def initialize_game(num_players):
    if num_players < 2:
        raise ValueError("At least 2 players are required to start the game.")

    if num_players > 6:
        raise ValueError("The maximum number of players allowed is 6.")

    # Create player objects
    players = []
    for player_id in range(num_players):
        player = {
            'id': player_id,
            'name': f'Player {player_id + 1}',  # Assign default names
            # Add any other player attributes as needed
        }
        players.append(player)

    # Initialize the game state
    game_state = {
        'players': players,
        'current_turn': 0,  # Initialize the turn to the first player
        'game_status': 'not_started',
        # Add other game-specific attributes as needed
    }

    # Return the initialized game state
    return game_state
