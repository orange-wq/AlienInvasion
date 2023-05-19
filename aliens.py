import pygame
from pygame.sprite import Sprite


class Alien(Sprite):

    def __init__(self, ai_game):
        super().__init__()
        self.settings = ai_game.settings
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.image = pygame.image.load('images/alien.png')
        self.rect = self.image.get_rect()
        self.x = self.rect.x

    def update(self):
        self.x += self.settings.aliens_speed * self.settings.aliens_direction
        self.rect.x = self.x

    def check_edges(self):
        if self.rect.right >= self.screen_rect.right or self.rect.left <= 0:
            return True
