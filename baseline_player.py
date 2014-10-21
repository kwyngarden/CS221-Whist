from player import Player
import util


class BaselinePlayer(Player):
    """Baseline computer player."""
    
    def choose_card(self, game_state):
        return util.strongest_legal_play(self.cards, game_state.trick.suit_led, game_state.trump)
