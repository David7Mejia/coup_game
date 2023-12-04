import random


class BotPlayer:
    def __init__(self, player_id):
        self.player_id = player_id

    def take_random_action(self, available_actions):
        # Simulate a random action selection for bot players
        return random.choice(available_actions)

    # def to_dict(self):
    #     # Convert the BotPlayer object to a dictionary
    #     return {'player_id': self.player_id}
