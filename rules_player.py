from player import Player
import util
import minimax

ATTEMPT_CUTOFF = 0.45
PARTNER_CUTOFF = 0.50
CLOSE_ENOUGH_FACTOR = 0.03

STRONG_UNLIKELY_FACTOR = 0.05


class RulesPlayer(Player):
    """Rule-Based computer player."""
    
    def choose_card(self, game_state):
        legalCards = util.get_legal_cards(self.cards, game_state.trick.suit_led)
        if (len(legalCards) == 1):
            # No point doing excessive processing if there's only one possible move
            return legalCards[0]
        
        #print "RULE CARDS", [(c.rank, c.suit) for c in self.cards]
        if True or len(game_state.cards_remaining) > 8:
            winProbs = [getWinProb(game_state, self, card) for card in legalCards]
        else:
            values = minimax.minimax_predict(self, game_state)
            legalCards = values.keys()
            winProbs = values.values()
        
        maxProb = max(winProbs)
        partnerWinProb = getWinProb(game_state, self, game_state.trick.card_of_player(game_state.get_partner(self)))
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
    numSlotsLed = getNumSlots(game_state, currPlayer, game_state.trick.suit_led, len(cardsUnknown))
    numSlotsTrump = getNumSlots(game_state, currPlayer, game_state.trick.trump, len(cardsUnknown))
    for antagonist in antagonistsLeft:
        if game_state.trick.suit_led not in game_state.player_possible_suits[antagonist]:
            probCanTrump = 1
        else: 
            numInSuit = len([c for c in cardsUnknown if c.suit == game_state.trick.suit_led])
            probCanTrump = 1
            for i in range(0, numCards):
                probCanTrump *= 1 - float(numInSuit) / (numSlotsLed - i)
                if probCanTrump == 0:
                    break
        #print probCanTrump
        sameSuits = [c for c in beatCards if c.suit == game_state.trick.suit_led]
        if game_state.trick.suit_led not in game_state.player_possible_suits[antagonist] or len(sameSuits) == 0:
            sameProb = 0
        else:
            sameProb = 1
            for i in range(0, numCards):
                beatProb = 1 - float(len(sameSuits)) / (numSlotsLed - i)
                sameProb *= beatProb
                if sameProb == 0:
                    break
            sameProb = 1 - sameProb
        trumpers = [c for c in beatCards if c.suit == game_state.trick.trump]
        if game_state.trick.trump != game_state.trick.suit_led and game_state.trick.trump not in game_state.player_possible_suits[antagonist]:
            trumpProb = 0
        elif len(trumpers) == 0:
            trumpProb = 0
        else:
            trumpProb = 1
            for i in range(0, numCards):
                beatProb = 1 - float(len(trumpers)) / (numSlotsTrump - i)
                trumpProb *= beatProb
                if trumpProb == 0:
                    break
            trumpProb = 1 - trumpProb
        mainProb *= 1 - sameProb - probCanTrump * trumpProb

    return mainProb

def getNumSlots(game_state, currPlayer, suit, numCardsOutstanding):
    numSlots = numCardsOutstanding
    thirdParties = list(game_state.get_opponents(currPlayer))
    thirdParties.append(game_state.get_partner(currPlayer))
    for party in thirdParties:
        if suit not in game_state.player_possible_suits[party.name]:
            numSlots -= len(party.cards)
    return numSlots


def getWeakestCard(game_state, legalCards):
    return util.weakest_card(legalCards, game_state.trick.trump)

def probSuitExists(cardsOutstanding, suit, numCardsHand):
    numLeft = len([c for c in cardsOutstanding if c.suit == suit])
    probNone = 1.0
    for i in range(0, numCardsHand):
        probNone *= 1 - float(numLeft) / (len(cardsOutstanding) - i)
    return 1 - probNone