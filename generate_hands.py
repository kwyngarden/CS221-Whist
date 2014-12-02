from card import suits
from deck import Deck

import copy
import random
import time


class HandGenerator:

    # Constructor
    def __init__(self, timeout=10, max_hands=20000):
        self.timeout = timeout
        self.max_hands = max_hands

    # Public interface of hand generator
    def generate_hands(self, game_state, player):
        other_player_cards = game_state.cards_remaining.difference(player.cards)
        other_players = [p.name for p in game_state.players if p.name != player.name]
        player_num_cards = {p.name: len(p.cards) for p in game_state.players}

        hand_assignments = self._generate_hands(
            other_player_cards,
            other_players,
            game_state.player_possible_suits,
            player_num_cards,
        )

        for hand_assignment in hand_assignments:
            hand_assignment[player.name] = set(player.cards)

        return hand_assignments

    # Hand generator
    # Params:
    #   cards_remaining: set of unplayed cards that have to be distributed to player hands
    #   players: list of names of players to distribute the cards to
    #   player_possible_suits: map of player name -> set of possible suits
    #   player_num_cards: map of player name -> number of cards that player has
    #
    # Usage: get a list of opponents + partners names (all but self), create a map of how many
    # cards each has (might not be the same if in the middle of a trick), create set of unplayed
    # cards minus the player's own cards, and pass in player_possible_suits as is.
    def _generate_hands(self, cards_remaining, players, player_possible_suits, player_num_cards):
        # Data structure used: set of assignments
        #   An assignment is a map from player name -> hand
        #       A hand is a set of cards
        hand_assignments = []
        partial_assignment = {player: set() for player in players}

        # Most constrained variable: order cards by number of players who can have that suit
        cards = self.order_cards_by_most_constrained(cards_remaining, players, player_possible_suits)

        # Run backtracking search assigning cards (variables) to players (domain)
        self.start_time = time.time()
        self.backtrack(cards, hand_assignments, players, player_possible_suits, player_num_cards, partial_assignment)

        return hand_assignments

    def backtrack(self, cards, hand_assignments, players, player_possible_suits, player_num_cards, partial_assignment):
        #print "Backtracking on %s, partial assignment %s" % (cards, partial_assignment)
        if not cards:
            hand_assignments.append(copy.deepcopy(partial_assignment))  
            return self.should_timeout() or len(hand_assignments) >= self.max_hands
        
        # Least constrained value: order players by number of cards left
        ordered_players = sorted(players, key=player_num_cards.get, reverse=True)

        card = cards[0]
        for player in ordered_players:
            # Check factors before continuing assignment
            if player_num_cards[player] > 0 and card.suit in player_possible_suits[player]:
                # Make assignment and backtrack
                partial_assignment[player].add(card)
                player_num_cards[player] -= 1
                should_stop = self.backtrack(cards[1:], hand_assignments, players, player_possible_suits, player_num_cards, partial_assignment)

                # Undo assignment
                partial_assignment[player].remove(card)
                player_num_cards[player] += 1

                if should_stop:
                    return True

    def should_timeout(self):
        if not self.start_time:
            return False
        return (time.time() - self.start_time) > self.timeout

    def order_cards_by_most_constrained(self, cards, players, player_possible_suits):
        suit_counts = {suit: 0 for suit in suits}
        for player in players:
            for suit in suits:
                if suit in player_possible_suits[player]:
                    suit_counts[suit] += 1
        return sorted(cards, key=lambda card: suit_counts[card.suit])

if __name__ == "__main__":
    gen = HandGenerator()
    players = ['P1', 'P2', 'P3']
    f = random.sample(Deck().cards, 9)
    player_num_cards = {player: 3 for player in players}
    player_possible_suits = {player: set(suits) for player in players}
    hand_assignments = gen._generate_hands(f, players, player_possible_suits, player_num_cards)
    print len(hand_assignments)

