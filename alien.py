import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """ A alien ship enemy for create to top corner screen """

    def __init__(self, ai_game):
        """ Initialize of elements """
        super().__init__()
        # Get main screen
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Set image of alien and get rect of images
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        # Set position of each Alien
        self.rect.y = self.rect.width
        self.rect.x = self.rect.height

        # Get exact horizontal position
        self.x = float(self.rect.x)

        

    def update(self):
        """ Update movement of alien """
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        self.rect.x = self.x

    def check_edges(self):
        """ Check edge of alien in screen """
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True
