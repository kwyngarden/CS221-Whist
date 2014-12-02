from player import Player
import util
import minimax

ATTEMPT_CUTOFF = 0.45
PARTNER_CUTOFF = 0.50
CLOSE_ENOUGH_FACTOR = 0.03

STRONG_UNLIKELY_FACTOR = 0.2

class RulesPlayer(Player):
    """Rule-Based computer player."""
    def choose_card(self, game_state):
        #print "RULE CARDS", [(c.rank, c.suit) for c in self.cards]
        if len(game_state.cards_remaining) > 8:
            legalCards = util.get_legal_cards(self.cards, game_state.trick.suit_led)
            winProbs = [getWinProb(game_state, self, card) for card in legalCards]
        else:
            values = minimax.minimax_predict(self, game_state)
            legalCards = values.keys()
            winProbs = values.values()
        maxProb = max(winProbs)
        partnerWinProb = getWinProb(game_state, self, game_state.trick.played.get(game_state.get_partner(self), None))
        if maxProb <= ATTEMPT_CUTOFF or partnerWinProb >= PARTNER_CUTOFF:
            return getWeakestCard(game_state, legalCards)
        winners = [card for card in legalCards if maxProb - winProbs[legalCards.index(card)] <= CLOSE_ENOUGH_FACTOR]
        #print "NUM WINNERS", len(winners)
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
        for card in modifiedBeatCards:
            unlikelyFactor = STRONG_UNLIKELY_FACTOR if card in game_state.unlikelies[antagonist] else 1
            beatProb = 1 - unlikelyFactor * (float(len(modifiedBeatCards)) / len(cardsUnknown))
            prob *= beatProb

def getWeakestCard(game_state, legalCards):
    # suits = {}
    # for card in legalCards:
    #     suitList = suits.get(card.suit, [])
    #     suitList.append(card)
    #     suits[card.suit] =  suitList
    # candidateSuit = None
    # candidateSuitFrac = 0.0
    # numTrumps = len(suits.get(game_state.trump, []))
    # if numTrumps > 0:
    #     for suit in suits:
    #         if suit != game_state.trick.trump and len(suits[suit]) == 1:
    #             toDiscard = suits[suit][0]
    #             remaining = set(game_state.cards_remaining)
    #             remaining = remaining.difference(legalCards)
    #             remaining = remaining.union(set([toDiscard]))
    #             if util.strongest_card(remaining, game_state.trick.suit_led, game_state.trump) != toDiscard:
    #                 #print "XXXXXXXXXXXXXXXXXXXXXXXXXXXHAPPENEDXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    #                 return toDiscard
    return util.weakest_card(legalCards, game_state.trick.trump)
