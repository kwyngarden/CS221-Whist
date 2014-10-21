class Player:
    """Abstract class for a Whist player. Subclasses must implement a strategy
    for playing a card in a given game and trick."""

    def __init__(self, name):
        self.name = name
        self.cards = []

    def choose_card(self, game_state):
        raise NotImplementedError("Strategy unimplemented")
