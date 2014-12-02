class Player:
    """Abstract class for a Whist player. Subclasses must implement a strategy
    for playing a card in a given game and trick."""

    def __init__(self, name):
        self.name = name
        self.cards = []

    """Called when a new round is starting so player can setup their strategy"""
    def round_start(self, game_state):
        return # default nothing happens

    """Ask the player to choose a card"""
    def choose_card(self, game_state):
        raise NotImplementedError("Strategy unimplemented")

    """Called when another player makes a play"""
    def observe_play(self, game_state, player, card):
        return # default nothing happens
