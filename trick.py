import util

class Trick:
    
    def __init__(self, players, trump):
        self.played = {}
        self.trump = trump
        self.suit_led = None
        self.left_to_play = set([player.name for player in players])

    def play_card(self, player, card):
        if not self.suit_led:
            self.suit_led = card.suit
        self.played[card] = player
        self.left_to_play.remove(player.name)
        player.cards.remove(card)

    def winning_card(self):
        return util.strongest_card([card for card in self.played], self.suit_led, self.trump)

    def winning_player(self):
        best_card = self.winning_card()
        return self.played[best_card] if best_card else None
