import pygame.font
from pygame.sprite import Group
from lives import Heart


class ScoreBoard:

    def __init__(self, ai_game):
        self.ai_game = ai_game
        self.settings = ai_game.settings
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.stats = ai_game.stats
        self.text_color = (0, 255, 0)
        self.font = pygame.font.SysFont(None, 48)
        self.prep_images()

    def prep_images(self):
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_lifes()

    def prep_score(self):
        rounded_score = round(self.stats.score)
        str_score = '{:,}'.format(rounded_score)
        self.score_image = self.font.render(str_score, True, self.text_color, self.settings.bg_color)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        rounded_score = round(self.stats.high_score)
        str_high_score = '{:,}'.format(rounded_score)
        self.high_score_image = self.font.render(str_high_score, True, self.text_color, self.settings.bg_color)
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.screen_rect.top

    def prep_level(self):
        str_level = str(self.stats.level)
        self.level_image = self.font.render(str_level, True, self.text_color, self.settings.bg_color)
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom

    def prep_lifes(self):
        self.lifes = Group()
        for lifes_number in range(self.stats.ship_limit):
            heart = Heart(self.ai_game)
            heart.rect.x = 10 + lifes_number * heart.rect.width
            heart.rect.y = 10
            self.lifes.add(heart)

    def check_high_score(self):
        if self.stats.high_score < self.stats.score:
            with open('record.txt', 'w') as fout:
                self.stats.high_score = self.stats.score
                fout.write(str(self.stats.high_score))
                self.prep_high_score()

    def draw_score(self):
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.lifes.draw(self.screen)
