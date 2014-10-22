import util


SCORE_TO_WIN = 30

class GameState:
    """Holds the state of the game."""

    def __init__(self, players, partners):
        self.players = players
        self.partners = partners
        self.trick = None
        self.trump = None
        self.cards_remaining = set()
        
        self.player_possible_suits = {}
        self.scores = {}
        for player in players:
            self.player_possible_suits[player.name] = set()
            self.scores[player.name] = 0

    def are_partners(self, player1_name, player2_name):
        return self.partners[player1_name] == player2_name

    def is_game_over(self):
        for player in self.players:
            if self.scores[player.name] + self.scores[self.partners[player.name]] >= SCORE_TO_WIN:
                return True
        return False

    def print_scores(self):
        self.print_team_score((self.players[0].name, self.partners[self.players[0].name]))
        self.print_team_score((self.players[1].name, self.partners[self.players[1].name]))
        print

    def print_team_score(self, players):
        player1, player2 = players
        print '\t%s (%s) and %s (%s) have a total score of %s' % (
            player1,
            self.scores[player1],
            player2,
            self.scores[player2],
            self.scores[player1] + self.scores[player2],
        )

    def __str__(self):
        out = ''
        out += 'Players: ' + str(self.players) + '\n'
        out += 'Partnerships: ' + str(self.partners) + '\n'
        out += 'Trump: ' + str(self.trump) + '\n'
        out += str(self.trick) + '\n'
        out += 'Unplayed cards: '
        for card in self.cards_remaining:
            out += '%s ' % card
        out += '\nPlayer possible suits: ' + str(self.player_possible_suits) + '\n'
        out += 'Scores: ' + str(self.scores)
        return out
