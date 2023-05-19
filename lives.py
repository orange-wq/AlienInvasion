import pygame
from pygame.sprite import Sprite


class Heart(Sprite):

    def __init__(self, ai_game):
        super().__init__()
        self.settings = ai_game.settings
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.image = pygame.image.load('images/new_heart.png')
        self.rect = self.image.get_rect()
