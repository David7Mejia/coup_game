from .models import GameState


def record_action(game_id, player_id, action):
    game_instance = GameState.objects.get(id=game_id)
    game_state = game_instance.get_game_state()

    if 'actions' not in game_state:
        game_state['actions'] = []

    game_state['actions'].append({'player_id': player_id, 'action': action})
    game_instance.set_game_state(game_state)
