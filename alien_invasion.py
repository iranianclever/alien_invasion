import sys
import pygame
# Adding settings attribution to the project
from settings import Settings
# Adding ship to game
from ship import Ship
# Adding bullet class
from bullet import Bullet


class AlienInvasion:
    ''' The game ship for distroy alien '''

    def __init__(self):
        ''' Initialization of game for run '''
        pygame.init()
        # Instance of settings
        self.settings = Settings()

        # Set screen mode to fullscreen
        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

        # Set screen mode
        self.screen = pygame.display.set_mode((self.settings.screen_width,
            self.settings.screen_height))

        # Set width and height of settings class
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        # Set caption game
        pygame.display.set_caption('Alien Invasion')
        # Create ship object
        self.ship = Ship(self)

        # A group bullet for manage live bullets
        self.bullets = pygame.sprite.Group()

    def run_game(self):
        ''' Run game '''
        while True:
            # Check event
            self._check_event()
            # Ship position update
            self.ship.update()
            # Update position of bullets and remove extra bullets
            self._update_bullets()
            # Update screen
            self._update_screen()

    def _update_bullets(self):
        """ Update position of bullets and Get rid of bullets to remove """
        # Set update position fo bullets
        self.bullets.update()
        # Get rid of bullets that have desappeared
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        print(len(self.bullets))

    def _check_event(self):
        ''' Check events and quit '''
        # Get event from input user
        for event in pygame.event.get():
            # Check type input for exit
            if event.type == pygame.QUIT:
                sys.exit(0)
            # Check type for key press
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            # Check type for button holding
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """ Respond to keypresses """
        # Check key for arrow right button
        if event.key == pygame.K_RIGHT:
            # Flag of move to right
            self.ship.move_right = True
        # Check key for arrow left button
        elif event.key == pygame.K_LEFT:
            # Flag of move to left
            self.ship.move_left = True
        # Check space key for shooting bullet
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        # Check key 'q' for exit
        elif event.key == pygame.K_q:
            # Exit form game
            sys.exit(0)

    def _check_keyup_events(self, event):
        """ Respond to keyup releases """
        # Check key for arrow right button
        if event.key == pygame.K_RIGHT:
            # Flag of move to right
            self.ship.move_right = False
        # Check key for arrow left button
        elif event.key == pygame.K_LEFT:
            # Flag of move to left
            self.ship.move_left = False

    def _fire_bullet(self):
        """ Create bullet and adding to group bullet sprite"""
        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_screen(self):
        ''' Elements of screen '''
        # Set background color
        self.screen.fill(self.settings.bg_color)
        # Draw ship in screen
        self.ship.blitme()
        # Update status of ship and movement
        self.ship.update()
        # Draw bullets in group
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        # Show screen object in loop
        pygame.display.flip()


# Main of program start
if __name__ == '__main__':
    # Create object
    ai = AlienInvasion()
    ai.run_game()
