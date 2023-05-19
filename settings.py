class Settings:

    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0, 0, 0)
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (255, 165, 0)
        self.bullets_allowed = 3
        self.aliens_drop_speed = 20
        self.ships_left = 3
        self.speedup_scale = 1.3
        self.aliens_scale = 1.5
        self.aliens_bullets_allowed = 5

    def initialize_dynamic_settings(self):
        self.ship_speed = 4.0
        self.bullet_speed = 4.0
        self.aliens_speed = 1.0
        self.aliens_direction = 1
        self.aliens_point = 50
        self.alien_bullet_speed = 2.0

    def increase_speed(self):
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.aliens_speed *= self.speedup_scale
        self.aliens_point = int(self.aliens_point * self.aliens_scale)
