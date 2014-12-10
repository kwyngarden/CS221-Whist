from player import Player
from monte_carlo import monte_carlo_simulate
import util

class MonteCarloOraclePlayer(Player):
    """Oracle that chooses cards by running Monte Carlo simulations on real hands"""

    MAX_SIMULATIONS = 2000

    def choose_card(self, game_state):
        legal_cards = util.get_legal_cards(self.cards, game_state.trick.suit_led)
        if (len(legal_cards) == 1):
            # No point doing excessive processing if there's only one possible move
            return legal_cards[0]

        utilitySums = {card: 0.0 for card in legal_cards}
        simulations_per_card = self.MAX_SIMULATIONS / len(legal_cards)
        
        for card in legal_cards:
            for _ in xrange(simulations_per_card):
                hands = {player.name: list(player.cards) for player in game_state.players}
                utilitySums[card] += monte_carlo_simulate(game_state, self, card, hands)

        return max(utilitySums.keys(), key=utilitySums.get)