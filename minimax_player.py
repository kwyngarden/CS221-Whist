from predictor import Predictor
import random, util

class MinimaxPlayer(Player):
    """Minimax player attempts to play with minimax rules."""

    def __init__(self, name, depth = 3):
        Base.__init__(self, name)
        self.depth = depth
        self.predictor = Predictor()
    
    def choose_card(self, game_state):
        legal_cards = util.get_legal_cards(self.cards, game_state.trick.suit_led)

    def observe_play(self, game_state, player, card):
        self.predictor.learn(game_state, player, card)
