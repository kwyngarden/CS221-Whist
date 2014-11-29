import util, copy

class Trick:
    
    def __init__(self, players, trump):
        self.played = {}
        self.trump = trump
        self.suit_led = None
        self.left_to_play = set([player.name for player in players])
        self.play_order = []

    def play_card(self, player, card):
        if not self.suit_led:
            self.suit_led = card.suit
        self.played[card] = player
        self.left_to_play.remove(player.name)
        self.play_order.append(player)

    def revert_play(self, player, card):
        assert (self.play_order)
        last = self.play_order.pop()
        assert (last == player)
        if not self.play_order:
            self.suit_led = None
        del self.played[card]
        self.left_to_play.add(player.name)

    def winning_card(self):
        return util.strongest_card([card for card in self.played], self.suit_led, self.trump)

    def winning_player(self):
        best_card = self.winning_card()
        return self.played[best_card] if best_card else None

    def partner_has_played(self, game_state, player):
        return game_state.get_partner(player).name not in self.left_to_play

    def get_opponents_yet_to_play(self, game_state, player):
        return [p for p in self.left_to_play if game_state.are_opponents(player.name, p)]

    def __str__(self):
        out = ''
        out += 'Played cards: '
        for card in self.played:
            out += '(%s, %s) ' % (card, self.played[card].name)
        out += '\nSuit led: ' + str(self.suit_led) + '\n'
        out += 'Players left to play: ' + str(self.left_to_play)
        return out
