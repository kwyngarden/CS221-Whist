SCORE_TO_WIN = 3

class GameState:
    """Holds the state of the game."""

    def __init__(self, players, partners):
        self.players = players
        self.partners = partners
        self.trick = None
        self.cards_remaining = set()
        
        self.player_possible_suits = {}
        self.scores = {}
        for player in players:
            self.player_possible_suits[player.name] = set()
            self.scores[player.name] = 0

    def are_partners(player1, player2):
        return self.partners[player1.name] == player2.name

    def is_game_over(self):
        for player in self.players:
            if self.scores[player.name] + self.scores[self.partners[player.name]] >= SCORE_TO_WIN:
                return True
        return False
