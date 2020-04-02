import pygame


class Ship:
    ''' Class ship for manage ship player '''

    def __init__(self, ai_game):
        """ Initialize the ship and set its starting position. """
        self.screen = ai_game.screen
        # Get settings of alien invasion
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()
        # Load the ship image and get its rect.
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        # Start each new ship at the bottom center of the screen.
        self.rect.midbottom = self.screen_rect.midbottom
        # Store decimal value for horizontal position
        self.x = float(self.rect.x)
        # Movement flag of right
        self.move_right = False
        # Movement flag of left
        self.move_left = False

    def update(self):
        """ Update movement by flag """
        # Check of flag right
        if self.move_right and self.rect.right < self.screen_rect.right:
            # Move to right
            self.x += self.settings.ship_speed
        # Check of flag left
        if self.move_left and self.rect.left > 0:
            # Move to left
            self.x -= self.settings.ship_speed
        # update rect x position with x temp
        self.rect.x = self.x

    def blitme(self):
        """ Draw the ship at its current location. """
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """ Set position of ship to screen center """
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
