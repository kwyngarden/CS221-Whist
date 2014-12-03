from player import Player
import util
import minimax

ATTEMPT_CUTOFF = 0.45
PARTNER_CUTOFF = 0.50
CLOSE_ENOUGH_FACTOR = 0.03

STRONG_UNLIKELY_FACTOR = 0.05
TRUMP_DANGER_FACTOR = 1

class RulesPlayer(Player):
    """Rule-Based computer player."""
    def choose_card(self, game_state):
        #print "RULE CARDS", [(c.rank, c.suit) for c in self.cards]
        if True or len(game_state.cards_remaining) > 8:
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
    beatCards = [c for c in cardsUnknown if util.strongest_card([c, card], game_state.trick.suit_led, game_state.trump) == c]
    mainProb = 1.0
    numCards = len(currPlayer.cards)
    for antagonist in antagonistsLeft:
        # prob1 = 1.0
        # prob2 = 1.0
        # sameSuits = [c for c in beatCards if c.suit == game_state.trick.suit_led]
        # trumpers = [c for c in beatCards if c.suit == game_state.trick.trump]
        # for i in range(0, numCards):
        #     beatProb1 = 1 - float(len(sameSuits)) / (len(cardsUnknown) - i)
        #     prob1 *= beatProb1
        #     probBeatenInSuit = 1 - prob1
        #     beatProb2 = 1 - float(len(trumpers)) / (len(cardsUnknown) - i)
        #     probBeatenTrumpSuit = 1 - prob2
        #     prob2 *= beatProb2
        # probInSuit = probSuitExists(cardsUnknown, game_state.trick.suit_led, numCards)
        # probInSuit = 0.0 if game_state.trick.suit_led not in game_state.player_possible_suits[antagonist] else probInSuit
        # probTrump = probSuitExists(cardsUnknown, game_state.trick.trump, numCards)
        # probInSuit = 0.0 if game_state.trick.trump not in game_state.player_possible_suits[antagonist] else probTrump
        # probBeaten = probInSuit * probBeatenInSuit + (1 - probInSuit) * probTrump * probBeatenTrumpSuit
        # mainProb *= 1 - probBeaten
        if game_state.trick.suit_led in game_state.player_possible_suits[antagonist]:
            trumpFactor = TRUMP_DANGER_FACTOR
            sameSuits = [c for c in beatCards if c.suit == game_state.trick.suit_led]
            for i in range(0, numCards):
                beatProb = 1 - float(len(sameSuits)) / (len(cardsUnknown) - i)
                mainProb *= beatProb
        elif game_state.trick.suit_led != game_state.trick.trump:
            trumpers = [c for c in beatCards if c.suit == game_state.trick.trump]
            for i in range(0, numCards):
                beatProb = 1 - float(len(trumpers)) / (len(cardsUnknown) - i)
                mainProb *= beatProb
    return mainProb

def getWeakestCard(game_state, legalCards):
    return util.weakest_card(legalCards, game_state.trick.trump)

def probSuitExists(cardsOutstanding, suit, numCardsHand):
    numLeft = len([c for c in cardsOutstanding if c.suit == suit])
    probNone = 1.0
    for i in range(0, numCardsHand):
        probNone *= 1 - float(numLeft) / (len(cardsOutstanding) - i)
    return 1 - probNone