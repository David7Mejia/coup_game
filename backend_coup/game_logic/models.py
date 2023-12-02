from django.db import models
import json

class GameState(models.Model):
    num_players = models.IntegerField()
    players = models.JSONField(default=list)  # Requires PostgreSQL or Django 3.1+
    current_turn = models.IntegerField(default=0)
    game_status = models.CharField(max_length=20, default='not_started')
    treasury = models.IntegerField()
    deck_card_counts = models.JSONField(default=dict)
    current_action = models.CharField(max_length=100, null=True, blank=True)
    current_action_player_id = models.IntegerField(null=True, blank=True)

    def set_game_state(self, state):
        for key, value in state.items():
            setattr(self, key, value)
        self.save()

    def get_game_state(self):
        return {
            "num_players": self.num_players,
            "players": self.players,
            "current_turn": self.current_turn,
            "game_status": self.game_status,
            "treasury": self.treasury,
            "deck_card_counts": self.deck_card_counts,
        }
