import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """ The Bullet ship, elements for shoot to aliens """

    def __init__(self, ai_game):
        """ Initialize objects of bullet """
        super().__init__()

        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = ai_game.settings.bullet_color

        # Create a bullet rect and set position
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width,
                                self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop

        # Store bullet position as a decimal value
        self.y = float(self.rect.y)

    def update(self):
        """ Move the bullet of the screen """
        # Update the decimal postion of the bullet
        self.y -= self.settings.bullet_speed
        # Update the rect postion
        self.rect.y = self.y

    def draw_bullet(self):
        """ Draw the bullet of the screen """
        pygame.draw.rect(self.screen, self.color, self.rect)
