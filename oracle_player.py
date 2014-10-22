from player import Player
import util

class OraclePlayer(Player):
    
    def get_auto_win_card(self, game_state):
        partner_name = game_state.partners[self.name]
        allies = [self.name, partner_name]
        partner_cards = util.get_player_with_name(game_state, partner_name).cards
        opponents = [player for player in game_state.players if player.name not in allies]

        # First, try finding a card that will let the oracle win.
        for card in self.cards:
            playable_opp_cards = []
            for opponent in opponents:
                suited = util.cards_by_suit(opponent.cards)
                if suited[card.suit]:
                    playable_opp_cards += suited[card.suit]
                elif suited[game_state.trump]:
                    playable_opp_cards += suited[game_state.trump]
            if not [opp_card for opp_card in playable_opp_cards if opp_card.is_stronger_than(card, card.suit, game_state.trump)]:
                return card

        # If no winners in own hand, try setting up a partner win
        for card in self.cards:
            playable_opp_cards = []
            for opponent in opponents:
                suited = util.cards_by_suit(opponent.cards)
                if suited[card.suit]:
                    playable_opp_cards += suited[card.suit]
                elif suited[game_state.trump]:
                    playable_opp_cards += suited[game_state.trump]

            playable_partner_cards = []    
            suited = util.cards_by_suit(partner_cards)
            if suited[card.suit]:
                playable_partner_cards += suited[card.suit]
            elif suited[game_state.trump]:
                playable_partner_cards += suited[game_state.trump]
            strongest_partner_card = util.strongest_card(playable_partner_cards, card.suit, game_state.trump)
            
            if strongest_partner_card and not [opp_card for opp_card in playable_opp_cards if opp_card.is_stronger_than(strongest_partner_card, card.suit, game_state.trump)]:
                return card
        
        return None

    def choose_card(self, game_state):
        # For the oracle, assume we go last and play the weakest card still winning
        legal_cards = util.get_legal_cards(self.cards, game_state.trick.suit_led)
        best_trick_card = game_state.trick.winning_card()
        winning_player = game_state.trick.winning_player()
        
        if not best_trick_card:
            # If the opponents could beat all cards in hand, we want to dump a
            # weak card; otherwise, we want to play an autowin card.
            auto_win_card = self.get_auto_win_card(game_state)
            return auto_win_card or min(legal_cards)

        winning_cards = [card for card in legal_cards if card.is_stronger_than(best_trick_card, game_state.trick.suit_led, game_state.trump)]
        if not winning_cards or game_state.are_partners(self.name, winning_player.name):
            # Don't try to win trick; get rid of weakest card
            return min(legal_cards)
            
        return min(winning_cards)
