from deck import Deck
import copy, operator

class Predictor:

    def __init__(self, threshold):
        self.deck = Deck()
        self.players = []
        self.card_prob = []
        self.threshold = threshold
        self.plays = set()
        self.trump = None
        self.suit_led = None

    def __copy__(self):
        clone = Predictor(self.threshold)
        clone.players = self.players
        clone.card_prob = [{card: prob for card, prob in probs.items()} for probs in self.card_prob]
        return clone

    """Setup/resets the predictor state so make sure 
       setup() is called before predict() or learn()"""
    def reset(self, game_state):
        self.players = game_state.players
        self.card_prob = [{card: 1.0 for card in self.deck.cards} for _ in xrange(len(self.players))]
        self.plays = set()
        self.trump = game_state.trump

    """Update model with information from game_state"""
    def refresh(self, game_state, current_player):
        index = self.players.index(current_player)
        # update suit led
        self.suit_led = game_state.trick.suit_led
        # we know the player's hand
        self.card_prob[index] = {card: 1.0 if card in current_player.cards else 0.0 for card in self.deck.cards}

    """Update model once we observe a player making a play"""
    def learn(self, player, card):
        for prob in self.card_prob:
            prob[card] = 0
        index = self.players.index(player)
        for c, p in self.card_prob[index].items():
            # if they did not follow suit they may not have the suit
            if self.suit_led and card.suit != self.suit_led:
                # if it's not trump either, they don't have trump either
                if card.suit != self.trump:
                    if c.suit == self.suit_led or c.suit == self.trump:
                        self.card_prob[index][c] = 0
                else: # don't have suit led
                    if c.suit == self.suit_led:
                        self.card_prob[index][c] = 0
            # decrease prob of cards with higher count
            if c.suit == card.suit and c > card:
                self.card_prob[index][c] *= 0.85
            # decrease prob of cards with lower count
            if c.suit == card.suit and c < card:
                self.card_prob[index][c] *= 0.95
        return

    """Returns a list of cards that we are fairly sure the player has"""
    def predict(self, player):
        index = self.players.index(player)
        return [card for card, prob in self.card_prob[index].items() if prob >= self.threshold and card not in self.plays]

    def try_play(self, card):
        self.plays.add(card)

    def revert_play(self, card):
        self.plays.remove(card)
