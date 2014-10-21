from card import Card, suits, ranks
from deck import Deck
from game_state import GameState
from trick import Trick

from player import Player
from baseline_player import BaselinePlayer
from human_player import HumanPlayer

import util

NUM_PLAYERS = 4
NUM_TRICKS = Deck.NUM_CARDS / NUM_PLAYERS

def get_players_and_partners():
    players = [
        HumanPlayer('player1'),
        BaselinePlayer('player2'),
        BaselinePlayer('player3'),
        BaselinePlayer('player4'),
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
    reset_player_possible_suits(game_state)
    game_state.trump = game_state.players[dealer_index].cards[-1].suit

def play_trick(game_state, first_to_play):
    game_state.trick = Trick(game_state.players, game_state.trump)
    turn_index = first_to_play
    
    for _ in xrange(NUM_PLAYERS):
        player = game_state.players[turn_index]
        card = player.choose_card(game_state)
        game_state.trick.play_card(player, card)
        game_state.cards_remaining.remove(card)
        print "%s played %s." % (player.name, card)
        turn_index = (turn_index + 1) % NUM_PLAYERS

    winning_player_name = game_state.trick.winning_player().name
    print "\nTrick was won by %s with %s.\n" % (winning_player_name, game_state.trick.winning_card())
    game_state.scores[winning_player_name] += 1
    return util.index_of_player_with_name(game_state, winning_player_name)

def play_deal(game_state, dealer_index, using_oracle=False):
    start_new_deal(game_state, dealer_index)
    print 'For this deal, the trump suit is %s.' % game_state.trump
    first_to_play = (dealer_index + 1) % NUM_PLAYERS
    
    # Play some tricks
    for trick_num in xrange(NUM_TRICKS):
        print '\n========== Beginning trick #%s. ==========\n' % (trick_num + 1)
        # util.print_hands(game_state)
        first_to_play = play_trick(game_state, first_to_play)
        if game_state.is_game_over():
            # The game ends as soon as the final trick is played
            return

def play_whist():
    players, partners = get_players_and_partners()
    game_state = GameState(players, partners)

    dealer_index = 0
    while not game_state.is_game_over():
        play_deal(game_state, dealer_index)
        dealer_index = (dealer_index + 1) % NUM_PLAYERS
        print 'Scores after deal: %s' % game_state.scores

    print 'Final scores: %s' % game_state.scores

if __name__ == '__main__':
    play_whist()
