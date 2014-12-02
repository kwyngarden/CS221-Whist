from trick import Trick
from generate_hands import HandGenerator
import collections, random, util

MINIMAX_DEPTH = 2

def minimax_values(player, game_state, players_hands):
    players = game_state.players
    turn_index = players.index(player)
    def vopt(hands, trick, depth):
        if depth == 0:
            return 0
        score = 0
        turn = (players.index(trick.play_order[-1]) + 1) % whist.NUM_PLAYERS
        # first we calculate the score if possible
        if not trick.left_to_play: # all players have played
            if game_state.are_partners(player.name, trick.winning_player().name):
                score = 1
            else:
                score = -1
            turn = players.index(trick.winning_player())
            if not players[turn].cards: # game complete
                return score
            trick = Trick(players, game_state.trump)
            depth = depth - 1
        # QUESTION: Does get_legal_cards also consider trump suite? How does human_player consider trump?
        cards = util.get_legal_cards(hands[players[turn]].name, trick.suit_led)
        plays = []
        # next we attempt to play cards
        if not cards: # this branch cannot be satisified, prune it
            return 0
        for card in cards[:]:
            trick.play_card(players[turn], card)
            hands[players[turn].name].remove(card)
            plays.append(score + vopt(hands, trick, depth))
            hands[players[turn].name].add(card)
            trick.revert_play(players[turn], card)
        # finally we return the highest score
        if game_state.are_partners(player.name, players[turn].name): # max
            return max(plays)
        else: # min
            return min(plays)
    # make best play
    legal_cards = util.get_legal_cards(player.cards, game_state.trick.suit_led)
    trick = game_state.trick
    choices = collections.Counter()
    for card in legal_cards[:]:
        trick.play_card(player, card)
        players_hands[player.name].remove(card)
        score = vopt(players_hands, trick, MINIMAX_DEPTH)
        players_hands[player.name].add(card)
        trick.revert_play(player, card)
        choices[card] = score

    return choices

def minimax_values(player, game_state):
    gen = HandGenerator()
    all_hands = gen.generate_hands(game_state, player)
    total = collections.Counter()
    for hands in all_hands:
        hands[player] = player.cards
        total += minimax_values(player, game_state, hands)
    all_scores = sum(vals.values())
    vals = {card: value * 1.0/all_scores for card, value in total.items()}
    print "values: %s" % vals
    return vals
