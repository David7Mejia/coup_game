def take_turn(player_id, action, target_player_id, target_card, game_state):
    player = next((plyr for plyr in game_state['players'] if plyr['id'] == player_id), None)
    target_player = next((plyr for plyr in game_state['players'] if plyr['id'] == target_player_id), None)

    if player is None or game_state['game_status'] != 'started':
        return False

    if player['coins'] >= 10:
        # Automatic coup due to having 10 or more coins
        if action != 'coup':
            return False  # Player must take the coup action
        else:
            # Continue with the coup
            pass

    if action == 'income':
        player['coins'] += 1
        game_state['treasury'] -= 1

    elif action == 'aid':
        player['coins'] += 2
        game_state['treasury'] -= 2

    # Handling coup action
    if action == 'coup':
        if player['coins'] >= 7:
            player['coins'] -= 7
            game_state['treasury'] += 7
            if target_player:
                # Initiate coup scenario
                game_state['temp_state'] = {
                    'waiting_for_target': True,
                    'target_player_id': target_player_id
                }
                return True
            else:
                return False
        else:
            return False

    # Check if it's time for the target player to lose influence
    if 'temp_state' in game_state and game_state['temp_state'].get('waiting_for_target', False):
        if player_id == target_player_id:
            # The target player chooses which card to discard
            if target_card in target_player['cards']:
                target_player['cards'].remove(target_card)
                # Additional logic for when a player loses all cards

                # Clear the temporary state
                del game_state['temp_state']
                return True
            else:
                return False

    return True
