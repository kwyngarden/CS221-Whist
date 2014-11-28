from deck import Deck
import copy, operator

class Predictor:

    def __init__(self):
        self.deck = Deck()
        self._players = []
        self.card_prob = []

    def __copy__(self):
        clone = type(self)()
        clone._players = self._players
        clone.card_prob = copy.deepcopy(self.card_prob)

    def setup(self, game_state):
        self._players = game_state.players
        self.card_prob = [{card: 1.0 for card in self.deck.cards} for _ in len(self._players)]

    def learn(self, game_state, player, card):
        if not self._players:
            self.setup(game_state)
        for prob in self.card_prob:
            prob[card] = 0
        return

    def predict(self, player):
        index = self._players.index(player)
        return max(self.card_prob[index].iteritems(), key=operator.itemgetter(1))[0]
