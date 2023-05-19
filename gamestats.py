class GameStats:

    def __init__(self, ai_game):
        self.settings = ai_game.settings
        self.game_active = False
        with open('record.txt', 'r') as fin:
            self.high_score = int(fin.readline().strip())
        self.reset_stats()

    def reset_stats(self):
        self.ship_limit = self.settings.ships_left
        self.score = 0
        self.level = 1
