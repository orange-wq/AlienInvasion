import sys
from time import sleep
from random import *
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from aliens import Alien
from gamestats import GameStats
from button import Button
from scoreboard import ScoreBoard
from aliens_bullet import AlienBullet


class AlienInvasion:

    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption('Alien Invasion')
        self.ship = Ship(self)
        self.stats = GameStats(self)
        self.play_button = Button(self, 'Play')
        self.sb = ScoreBoard(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.aliens_bullets = pygame.sprite.Group()
        self.create_fleet()
        self.bg = pygame.image.load('images/space_3.jpg')

    def run_game(self):
        while True:
            self.check_event()
            if self.stats.game_active:
                self.ship.update()
                self.bullets.update()
                self.update_bullets()
                self.update_aliens()
                self.aliens_bullets.update()
            self.update_screen()

    def update_screen(self):
        self.screen.blit(self.bg, (0, 0))
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        if not self.stats.game_active:
            self.play_button.draw_button()
        self.sb.draw_score()
        self.aliens_bullets.draw(self.screen)
        pygame.display.flip()

    def restart(self):
        if self.stats.ship_limit > 0:
            self.aliens_bullets.empty()
            self.aliens.empty()
            self.bullets.empty()
            self.ship.center_ship()
            self.create_fleet()
            sleep(0.5)
        else:
            self.stats.game_active = False
            self.play_button.draw_button()
            pygame.mouse.set_visible(True)

    def check_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self.check_play_button(mouse_pos)

    def check_play_button(self, mouse_pos):
        if self.play_button.rect.collidepoint(mouse_pos) and not self.stats.game_active:
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_lifes()
            self.stats.game_active = True
            self.restart()
            pygame.mouse.set_visible(False)

    def _check_keydown(self, event):
        if event.key == pygame.K_w:
            self.ship.moving_up = True
        elif event.key == pygame.K_s:
            self.ship.moving_down = True
        elif event.key == pygame.K_d:
            self.ship.moving_right = True
        elif event.key == pygame.K_a:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_q:
            sys.exit()

    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def update_bullets(self):
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self.check_collisions()

    def check_collisions(self):
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:
            for alien in collisions.values():
                self.stats.score += self.settings.aliens_point * len(alien)
                self.sb.prep_score()
                self.sb.check_high_score()

    def _check_keyup(self, event):
        if event.key == pygame.K_w:
            self.ship.moving_up = False
        elif event.key == pygame.K_s:
            self.ship.moving_down = False
        elif event.key == pygame.K_d:
            self.ship.moving_right = False
        elif event.key == pygame.K_a:
            self.ship.moving_left = False

    def create_fleet(self):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - 2 * alien_width
        available_space_y = self.settings.screen_height - 2 * alien_height
        number_aliens_x = available_space_x // (2 * alien_width)
        number_aliens_y = available_space_y // (4 * alien_height)
        for row in range(number_aliens_y):
            for line in range(number_aliens_x):
                self._create_alien(line, row)

    def _create_alien(self, line, row):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * line
        alien.y = alien_height + 2 * alien_height * row + 30
        alien.rect.x = alien.x
        alien.rect.y = alien.y
        self.aliens.add(alien)

    def fire_aliens_bullet(self):
        if len(self.aliens_bullets) < self.settings.aliens_bullets_allowed:
            attacking_alien = choice(self.aliens.sprites())
            alien_bullet = AlienBullet(self, attacking_alien.rect.centerx, attacking_alien.rect.bottom)
            self.aliens_bullets.add(alien_bullet)

    def _check_aliens_bullets(self):
        for bullet in self.aliens_bullets.copy():
            if bullet.rect.top >= self.settings.screen_height:
                self.aliens_bullets.remove(bullet)

    def _check_aliens_bullets_collisions(self):
        if pygame.sprite.spritecollideany(self.ship, self.aliens_bullets):
            self.stats.ship_limit -= 1
            self.sb.prep_lifes()
            self.restart()

    def update_aliens(self):
        self.aliens.update()
        self.check_aliens_direction()
        self.check_aliens_bottom()
        self.check_sprites_collisions()
        self.fire_aliens_bullet()
        self._check_aliens_bullets()
        self._check_aliens_bullets_collisions()
        if not self.aliens:
            self.start_new_level()

    def start_new_level(self):
        self.stats.level += 1
        self.sb.prep_level()
        self.settings.increase_speed()
        self.restart()

    def check_aliens_direction(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_aliens_direction()
                break

    def _change_aliens_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.aliens_drop_speed
        self.settings.aliens_direction *= -1

    def check_aliens_bottom(self):
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                self.stats.ship_limit -= 1
                self.sb.prep_lifes()
                self.restart()
                break

    def check_sprites_collisions(self):
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self.stats.ship_limit -= 1
            self.sb.prep_lifes()
            self.restart()


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
