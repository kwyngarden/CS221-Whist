from card import Card, suits, ranks
from deck import Deck
from game_state import GameState
from trick import Trick

from player import Player
from baseline_player import BaselinePlayer
from human_player import HumanPlayer
from oracle_player import OraclePlayer

import random
import util

NUM_PLAYERS = 4
NUM_TRICKS = Deck.NUM_CARDS / NUM_PLAYERS

def get_players_and_partners():
    players = [
        HumanPlayer('Human'),
        BaselinePlayer('OpponentBaseline1'),
        OraclePlayer('OraclePlayer'),
        BaselinePlayer('OpponentBaseline2'),
    ]
    partners = {
        players[0].name: players[2].name,
        players[1].name: players[3].name,
        players[2].name: players[0].name,
        players[3].name: players[1].name,
    }
    return players, partners

def reset_player_possible_suits(game_state):
    for player in game_state.players:
        game_state.player_possible_suits[player.name] = set(suits)

def start_new_deal(game_state, dealer_index):
    deck = Deck()
    game_state.cards_remaining = set(deck.cards)
    hands = deck.deal()
    for i in xrange(NUM_PLAYERS):
        game_state.players[i].cards = hands[i]
        game_state.players[i].round_start(game_state)
    reset_player_possible_suits(game_state)
    game_state.trump = game_state.players[dealer_index].cards[-1].suit

def play_trick(game_state, first_to_play):
    game_state.trick = Trick(game_state.players, game_state.trump)
    turn_index = first_to_play

    for _ in xrange(NUM_PLAYERS):
        player = game_state.players[turn_index]
        card = player.choose_card(game_state)
        game_state.trick.play_card(player, card)
        player.cards.remove(card)
        game_state.cards_remaining.remove(card)
        if not game_state.has_card_of_suit(card.suit):
            for everyPlayer in game_state.players:
                game_state.player_possible_suits[everyPlayer.name].discard(card.suit)
        if card.suit != game_state.trick.suit_led:
            game_state.player_possible_suits[player.name].discard(game_state.trick.suit_led)

        print "%s played %s." % (player.name, card)
        # each other player observes this play
        for opponent in game_state.players:
            if opponent != player:
                opponent.observe_play(game_state, player, card)
        turn_index = (turn_index + 1) % NUM_PLAYERS

    winning_player_name = game_state.trick.winning_player().name
    print "\nTrick was won by %s with %s.\n" % (winning_player_name, game_state.trick.winning_card())
    game_state.scores[winning_player_name] += 1
    return util.index_of_player_with_name(game_state, winning_player_name)

def play_deal(game_state, dealer_index, using_oracle=False):
    start_new_deal(game_state, dealer_index)
    
    print '\nBefore this deal, the scores are as follows:'
    game_state.print_scores()
    
    print '\n\n--------------- Beginning new deal ---------------'
    print 'For this deal, the trump suit is %s.' % game_state.trump
    first_to_play = (dealer_index + 1) % NUM_PLAYERS
    
    # Play some tricks
    for trick_num in xrange(NUM_TRICKS):
        print '\n========== Beginning trick #%s (trump is %s) ==========\n' % (trick_num + 1, game_state.trump)
        # util.print_hands(game_state)
        first_to_play = play_trick(game_state, first_to_play)

def play_whist():
    players, partners = get_players_and_partners()
    game_state = GameState(players, partners)

    dealer_index = 0
    while not game_state.is_game_over():
        play_deal(game_state, dealer_index)
        dealer_index = (dealer_index + 1) % NUM_PLAYERS

    print 'The game is over! Final scores:'
    game_state.print_scores()

# ORACLE CODE

def play_oracle_whist(num_iters=1000, silent=True):
    random.seed(42)
    players, partners, oracle_name = get_oracle_players_and_partners()
    allies = ['Oracle1', 'Oracle2']
    opponents = ['OpponentBaseline1', 'OpponentBaseline2']
    oracle_wins = 0
    opponent_wins = 0
    points_for = 0
    points_against = 0
    
    for _ in xrange(num_iters):
        game_state = GameState(players, partners)

        dealer_index = 0
        while not game_state.is_game_over():
            play_oracle_deal(game_state, dealer_index, oracle_name, silent=silent)
            dealer_index = (dealer_index + 1) % NUM_PLAYERS
            #raw_input()
        
        if not silent:
            print 'The game is over! Final scores:'
            game_state.print_scores()
        
        ally_score = sum([game_state.scores[ally] for ally in allies])
        opp_score = sum([game_state.scores[opp] for opp in opponents])
        if ally_score > opp_score:
            oracle_wins += 1
        else:
            opponent_wins += 1
        points_for += ally_score
        points_against += opp_score

    print "Oracle record: %s-%s" % (oracle_wins, opponent_wins)
    print "Points for: %s" % points_for
    print "Points against: %s" % points_against

def get_oracle_players_and_partners():
    players = [
        # BaselinePlayer('OpponentBaseline1'),
        OraclePlayer('Oracle1'),
        BaselinePlayer('OpponentBaseline2'),
        OraclePlayer('Oracle2'),
        BaselinePlayer('OpponentBaseline1'),
    ]
    partners = {
        players[0].name: players[2].name,
        players[1].name: players[3].name,
        players[2].name: players[0].name,
        players[3].name: players[1].name,
    }
    return players, partners, players[0].name

def play_oracle_deal(game_state, dealer_index, oracle_name, silent=False):
    start_new_deal(game_state, dealer_index)
    
    if not silent:
        print '\nBefore this deal, the scores are as follows:'
        game_state.print_scores()

        print '\n\n--------------- Beginning new deal ---------------'
        print 'For this deal, the trump suit is %s.' % game_state.trump
    first_to_play = (dealer_index + 1) % NUM_PLAYERS
    
    # Play some tricks
    for trick_num in xrange(NUM_TRICKS):
        if not silent:
            print '\n========== Beginning trick #%s (trump is %s) ==========\n' % (trick_num + 1, game_state.trump)
            util.print_hands(game_state)
        first_to_play = play_oracle_trick(game_state, first_to_play, silent=silent)
        if not silent:
            raw_input()

def play_oracle_trick(game_state, first_to_play, silent=False):
    game_state.trick = Trick(game_state.players, game_state.trump)
    turn_index = first_to_play
    
    for i in xrange(NUM_PLAYERS):
        player = game_state.players[turn_index]
        card = player.choose_card(game_state)
        game_state.trick.play_card(player, card)
        player.cards.remove(card)
        game_state.cards_remaining.remove(card)
        if not game_state.has_card_of_suit(card.suit):
            for everyPlayer in game_state.players:
                game_state.player_possible_suits[everyPlayer.name].discard(card.suit)
        if card.suit != game_state.trick.suit_led:
            game_state.player_possible_suits[player.name].discard(game_state.trick.suit_led)
        if not silent:
            print "%s played %s." % (player.name, card)
        turn_index = (turn_index + 1) % NUM_PLAYERS

    winning_player_name = game_state.trick.winning_player().name
    if not silent:
        print "\nTrick was won by %s with %s.\n" % (winning_player_name, game_state.trick.winning_card())
    game_state.scores[winning_player_name] += 1
    return util.index_of_player_with_name(game_state, winning_player_name)

if __name__ == '__main__':
    play_whist()
    # play_oracle_whist(silent=True, num_iters=10000)