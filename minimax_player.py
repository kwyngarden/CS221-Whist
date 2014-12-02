from player import Player
from predictor import Predictor
from trick import Trick
import random, util, copy

class MinimaxPlayer(Player):
    """Minimax player attempts to play with minimax rules."""
    THRESHOLD = 0.8

    def __init__(self, name, depth = 2, breadth = 3):
        Player.__init__(self, name)
        self.depth = depth
        self.breadth = breadth
        self.predictor = Predictor(self.THRESHOLD)

    def round_start(self, game_state):
        self.predictor.reset(game_state)
    
    def choose_card(self, game_state):
        self.predictor.refresh(game_state, self)
        players = self.predictor.players
        turn_index = players.index(self)
        def vopt(pred, trick, depth):
            if depth == 0:
                return 0
            score = 0
            turn = (players.index(trick.play_order[-1]) + 1) % whist.NUM_PLAYERS
            # first we calculate the score if possible
            if not trick.left_to_play: # all players have played
                if game_state.are_partners(self.name, trick.winning_player().name):
                    score = 1
                else:
                    score = -1
                turn = players.index(trick.winning_player())
                if not players[turn].cards: # game complete
                    return score
                trick = Trick(players, game_state.trump)
                depth = depth - 1
            # QUESTION: Does get_legal_cards also consider trump suite? How does human_player consider trump?
            cards = util.get_legal_cards(pred.predict(players[turn]), trick.suit_led)
            cards = cards if len(cards) < self.breadth else random.sample(cards, self.breadth)
            plays = []
            # next we attempt to play cards
            if not cards: # this branch cannot be satisified, prune it
                return 0
            for card in cards:
                trick.play_card(players[turn], card)
                pred.try_play(card)
                plays.append(score + vopt(pred, trick, depth))
                pred.revert_play(card)
                trick.revert_play(players[turn], card)
            # finally we return the highest score
            if game_state.are_partners(self.name, players[turn].name): # max
                return max(plays)
            else: # min
                return min(plays)
        # make best play
        legal_cards = util.get_legal_cards(self.cards, game_state.trick.suit_led)
        trick = game_state.trick
        pred = self.predictor
        choices = []
        max_score = float("-inf")
        for card in legal_cards:
            trick.play_card(self, card)
            pred.try_play(card)
            score = vopt(pred, trick, self.depth)
            pred.revert_play(card)
            trick.revert_play(self, card)
            print "Predict %s: %d" % (card, score)
            choices.append((score, card))
            if score > max_score:
                max_score = score

        choices = [card for score, card in choices if score == max_score]
        max_card = random.choice(choices)
        pred.learn(self, max_card)
        return max_card

    def observe_play(self, game_state, player, card):
        self.predictor.refresh(game_state, self)
        self.predictor.learn(player, card)

import whist # for constants
