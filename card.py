suits = ['Hearts', 'Clubs', 'Diamonds', 'Spades']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']

class Card:
    
    def __init__(self, suit, rank):
        self.suit = suit.capitalize()
        self.rank = rank.capitalize()

    def is_stronger_than(other_card, suit_led, trump):
        if other_card.suit == trump:
            return self.suit == trump and self > other_card
        if self.suit == trump:
            return other_card.suit != trump or self > other_card
        if other_card.suit == suit_led:
            return self.suit == suit_led and self > other_card
        if self.suit == suit_led:
            return other_card.suit != suit_led or self > other_card
        return self > other_card
    
    def __str__(self):
        return self.rank + '-' + self.suit

    def __lt__(self, other):
        return ranks.index(self.rank) < ranks.index(other.rank)

    def __eq__(self, other):
        if type(self) is type(other):
            return self.suit == other.suit and self.rank == other.rank
        else:
            return false

    def __hash__(self):
        return 23 * self.rank.__hash__() + 37 * self.suit.__hash__()
    
    def __ne__(self, other):
        if type(self) is type(other):
            return self.suit != other.suit or self.rank != other.rank
        else:
            return True