from card import suits, suit_symbols
from player import Player
import util


class HumanPlayer(Player):
    """Human player which chooses cards through stdin."""
    
    def choose_card(self, game_state):
        legal_cards = util.get_legal_cards(self.cards, game_state.trick.suit_led)
        suited = util.cards_by_suit(legal_cards)
        sorted_options = []
        for suit in suits:
            sorted_options += suited[suit]
        
        print "\n\tIt's your (%s) turn to pick a card! Your hand looks like this:" % self.name
        util.print_cards(self.cards, num_tabs=2)
        
        if game_state.trick.played:
            winning_player = game_state.trick.winning_player().name
            winning_card = game_state.trick.winning_card()
            print "\t%s is currently winning with %s." % (winning_player, winning_card)

        if game_state.trick.suit_led:
            print "\t%s %s was led and %s %s is trump. Your options are:" % (
                game_state.trick.suit_led, suit_symbols[game_state.trick.suit_led],
                game_state.trump, suit_symbols[game_state.trump])
        else:
            print "\tYou are the first to play and trump is %s. Your options are:" % game_state.trump
        for i in xrange(len(sorted_options)):
            print "\t\t%s: %s" % (i + 1, sorted_options[i])
        message = "\tPlease enter the number corresponding to your choice: "
        selected = util.get_valid_number(1, len(sorted_options), message, indent=2)
        print

        return sorted_options[selected - 1]
