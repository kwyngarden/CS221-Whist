import util, copy

class Trick:
    
    def __init__(self, players, trump):
        self.played = {}
        self.trump = trump
        self.suit_led = None
        self.left_to_play = set([player.name for player in players])
        self.last_player = None

    def __copy__(self):
        clone = type(self)([], self.trump)
        clone.played = dict(self.played)
        clone.suit_led = self.suit_led
        clone.left_to_play = set(self.left_to_play)
        clone.last_player = self.last_player

    def play_card(self, player, card):
        if not self.suit_led:
            self.suit_led = card.suit
        self.played[card] = player
        self.left_to_play.remove(player.name)
        self.last_player = player

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
