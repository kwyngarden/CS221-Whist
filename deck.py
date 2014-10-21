from card import Card, suits, ranks
from random import shuffle

class Deck:
    NUM_CARDS = 52
    
    def __init__(self):
        self.cards = []
        for suit in suits:
            for rank in ranks:
                self.cards.append(Card(suit, rank))
        shuffle(self.cards)
    
    def deal(self):
        return self.cards[:13], self.cards[13:26], self.cards[26:39], self.cards[39:]

    def __str__(self):
        card_strings = [str(card) for card in self.cards]
        return ' '.join(card_strings)
