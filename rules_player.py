from player import Player
import util

ATTEMPT_CUTOFF = 0.45
PARTNER_CUTOFF = 0.50
CLOSE_ENOUGH_FACTOR = 0.03

class RulesPlayer(Player):
    """Rule-Based computer player."""
    def choose_card(self, game_state):
        #print "RULE CARDS", [(c.rank, c.suit) for c in self.cards]
        legalCards = util.get_legal_cards(self.cards, game_state.trick.suit_led)
        winProbs = [getWinProb(game_state, self, card) for card in legalCards]
        maxProb = max(winProbs)
        partnerWinProb = getWinProb(game_state, self, game_state.trick.played.get(game_state.get_partner(self), None))
        if maxProb <= ATTEMPT_CUTOFF or partnerWinProb >= PARTNER_CUTOFF:
            return getWeakestCard(game_state, legalCards)
        winners = [card for card in legalCards if maxProb - winProbs[legalCards.index(card)] <= CLOSE_ENOUGH_FACTOR]
        return min(winners)

def getWinProb(game_state, currPlayer, card):
    if card is None:
        return 0.0
    combinedPool = game_state.trick.played.keys()
    combinedPool.append(card)
    if util.strongest_card(combinedPool, game_state.trick.suit_led, game_state.trump) != card:
        return 0.0
    antagonistsLeft = game_state.trick.get_opponents_yet_to_play(game_state, currPlayer)
    if len(antagonistsLeft) == 0:
        return 1.0
    cardsUnknown = set(game_state.cards_remaining)
    cardsUnknown = cardsUnknown.difference(game_state.trick.played.keys())
    cardsUnknown = cardsUnknown.difference(currPlayer.cards)
    beatCards = [c for c in cardsUnknown if c > card]
    prob = 1.0
    for antagonist in antagonistsLeft:
        modifiedBeatCards = [c for c in beatCards if c.suit in game_state.player_possible_suits[antagonist]]
        beatProb = 1 - float(len(modifiedBeatCards)) / len(cardsUnknown)
        prob *= beatProb ** len(currPlayer.cards)
    return prob

def getWeakestCard(game_state, legalCards):
    return util.weakest_card(legalCards, game_state.trick.trump)
