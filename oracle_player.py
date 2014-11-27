from player import Player
import util

DEBUG = False

class OraclePlayer(Player):

    def choose_card(self, game_state):
        if not game_state.trick.winning_card():
            # If we are the first to play, we can try finding a card that guarantees a win
            auto_win_card = self.get_auto_win_card(game_state)
            if auto_win_card:
                if DEBUG: print '\t[DEBUG] %s is the first to play and found an auto-win card: %s' % (self.name, auto_win_card)
                return auto_win_card

        # Otherwise, try deferring to partner first
        if self.partner_can_win_trick(game_state):
            card_to_dump = self.dump_card(game_state)
            if DEBUG: print '\t[DEBUG] %s realizes partner can win trick, so dumping %s' % (self.name, card_to_dump)
            return card_to_dump

        winning_card = self.get_weakest_winning_card_or_none(game_state)
        if winning_card:
            if DEBUG: print '\t[DEBUG] %s\'s partner cannot win, but found the weakest winning card %s' % (self.name, winning_card)
            return winning_card
        else:
            card_to_dump = self.dump_card(game_state)
            if DEBUG: print '\t[DEBUG] %s (or partner) cannot win, so dumping card %s' % (self.name, card_to_dump)
            return card_to_dump

    def get_weakest_winning_card_or_none(self, game_state):
        opponents_yet_to_play = game_state.trick.get_opponents_yet_to_play(game_state, self)
        opponent_cards = []
        if game_state.trick.winning_card():
            opponent_cards.append(game_state.trick.winning_card())
        for opponent_name in opponents_yet_to_play:
            opponent = util.get_player_with_name(game_state, opponent_name)
            opponent_legal_cards = util.get_legal_cards(opponent.cards, game_state.trick.suit_led)
            opponent_strongest_card = util.strongest_card(opponent_legal_cards, game_state.trick.suit_led, game_state.trump)
            opponent_cards.append(opponent_strongest_card)

        strongest_opponent_card = util.strongest_card(opponent_cards, game_state.trick.suit_led, game_state.trump)
        winning_cards = []
        for card in util.get_legal_cards(self.cards, game_state.trick.suit_led):
            if card.is_stronger_than(strongest_opponent_card, game_state.trick.suit_led, game_state.trump):
                winning_cards.append(card)

        weakest_winning_card = util.weakest_card(winning_cards, game_state.trump)
        return weakest_winning_card or None

    def dump_card(self, game_state):
        legal_cards = util.get_legal_cards(self.cards, game_state.trick.suit_led)
        # Complicated logic...
        return util.weakest_card(legal_cards, game_state.trump)

    def partner_can_win_trick(self, game_state):
        partner = game_state.get_partner(self)
        opponents_to_play = game_state.trick.get_opponents_yet_to_play(game_state, self)
        partner_is_winning = (game_state.trick.winning_player() is not None) and \
            (game_state.trick.winning_player().name == partner.name)
        if DEBUG: print '\t[DEBUG] %s looks if partner can win. Currently winning? %s, Opponents to play: %s' % (self.name, partner_is_winning, opponents_to_play)

        # If no opponents are left, this is simply whether the partner is winning
        if not opponents_to_play:
            if DEBUG: print '\t\t[DEBUG] %s: No opponents left to play, so returning whether partner is winning.' % (self.name)
            return partner_is_winning
        
        if game_state.trick.partner_has_played(game_state, self):
            if not partner_is_winning:
                # If partner has already played and isn't winning, they won't win the trick
                if DEBUG: print '\t\t[DEBUG] %s: Partner played but is not winning, so returning false' % (self.name)
                return False
            partner_card = game_state.trick.winning_card()
        else:
            # Assume partner tries to win trick
            partner_legal_cards = util.get_legal_cards(partner.cards, game_state.trick.suit_led)
            partner_card = util.strongest_card(partner_legal_cards, game_state.trick.suit_led, game_state.trump)
            if (game_state.trick.winning_card() is not None) and \
                (not partner_card.is_stronger_than(game_state.trick.winning_card(), game_state.trick.suit_led, game_state.trump)):
                return False
        if DEBUG: print '\t\t[DEBUG] %s: Partner has best card or played card of %s' % (self.name, partner_card)
        
        for opponent_name in opponents_to_play:
            opponent = util.get_player_with_name(game_state, opponent_name)
            opponent_legal_cards = util.get_legal_cards(opponent.cards, game_state.trick.suit_led)
            opponent_strongest_card = util.strongest_card(opponent_legal_cards, game_state.trick.suit_led, game_state.trump)
            if opponent_strongest_card.is_stronger_than(partner_card, game_state.trick.suit_led, game_state.trump):
                if DEBUG: print '\t\t[DEBUG] %s: Partner\'s strongest card is beaten by opponent %s with card %s' % (self.name, opponent_name, opponent_strongest_card)
                return False

        return True # No opponent can beat partner's (played or best) card

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

    def choose_card_cheating(self, game_state):
        # For the cheating oracle, assume we go last and play the weakest card still winning
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
