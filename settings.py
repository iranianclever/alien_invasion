
class Settings:
    ''' Settings of game '''

    def __init__(self):
        ''' Initialization of settings game '''
        # Screen width
        self.screen_width = 1200
        # Screen height
        self.screen_height = 800
        # Values of background color
        self.bg_color = (230, 230, 230)
        # Ship speed
        self.ship_speed = 1.5

        # Bullet settings
        self.bullet_speed = 1.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullet_allowed = 3

        # Alien settings
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10
        self.fleet_direction = 1
