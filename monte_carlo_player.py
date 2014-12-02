from monte_carlo import monte_carlo_utilities
from player import Player


class MonteCarloPlayer(Player):

    def choose_card(self, game_state):
        utilities = monte_carlo_utilities(game_state, self)
        sorted_cards = sorted(utilities.keys(), key=utilities.get, reverse=True)
        return sorted_cards[0]