import pygame
from pygame.sprite import Sprite


class AlienBullet(Sprite):

    def __init__(self, ai_game, x, y):
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.image = pygame.image.load('images/alien_bullet_new.png')
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        self.rect.y += self.settings.alien_bullet_speed
