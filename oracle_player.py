import util

class OraclePlayer(Player):
    
    def choose_card(self, game_state):
        # For the oracle, assume we go last and play the weakest card still winning
        best_trick_card = game_state.trick.winning_card()
        winning_player = game_state.trick.winning_player()
        legal_cards = util.get_legal_cards(self.cards, game_state.trick.suit_led)
        
        winning_cards = [card for card in legal_cards if card.is_stronger_than(best_trick_card)]
        if not winning_cards or game_state.are_partners(self, winning_player):
            # Don't try to win trick; get rid of weakest card
            return min(legal_cards)
            
        return weakest_card(winning_cards)
