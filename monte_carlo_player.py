from monte_carlo import monte_carlo_utilities
from player import Player
import util


class MonteCarloPlayer(Player):

    def choose_card(self, game_state):
        legalCards = util.get_legal_cards(self.cards, game_state.trick.suit_led)
        if (len(legalCards) == 1):
            # No point doing excessive processing if there's only one possible move
            return legalCards[0]

        utilities = monte_carlo_utilities(game_state, self)
        sorted_cards = sorted(utilities.keys(), key=utilities.get, reverse=True)
        return sorted_cards[0]