import sys
from time import sleep
import pygame
# Adding settings attribution to the project
from settings import Settings
# Adding ship to game
from ship import Ship
# Adding bullet class
from bullet import Bullet
# Adding alien class
from alien import Alien
# Adding game stats class
from game_stats import GameStats
# Adding scoreboard class
from scoreboard import Scoreboard
# Adding button class
from button import Button


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
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))

        # Set width and height of settings class
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        # Set caption game
        pygame.display.set_caption('Alien Invasion')


        # Create an instace to store game statistics,
        # and create a scoreboard.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        # Create ship object
        self.ship = Ship(self)

        # A group bullet for manage live bullets
        self.bullets = pygame.sprite.Group()

        # A group of alien
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # Make a instance of button class
        self.play_button = Button(self, 'Play')

    def _ship_hit(self):
        """ Response to hit ship """
        if self.stats.ships_left > 0:
            # Decrement ships_left, and update scoreboard
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            # Empty aliens and bullets from screen
            self.aliens.empty()
            self.bullets.empty()
            # Create a fleet aliens
            self._create_fleet()
            # Set position of ship
            self.ship.center_ship()
            # Set sleep of game
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_fleet_edges(self):
        """ Check aliens of edge and change fleet direction """
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """ Change fleet direction of aline """
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _create_fleet(self):
        """ Create a fleet of aliens """
        # Create a instance of alien class
        alien = Alien(self)
        # Get width of a alien
        alien_width, alien_height = alien.rect.size
        # Calculate available space of screen
        available_space_x = self.settings.screen_width - (2 * alien_width)
        # Calculate count of aliens
        number_aliens_x = available_space_x // (2 * alien_width)

        # Determine the number of rows of aliens that fit on the screen.
        ship_height = self.ship.rect.height

        available_space_y = (self.settings.screen_height -
                             (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # Calculate space of each aliens and to group
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """ Create a sample alien """
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        # Add alien to sprite group
        self.aliens.add(alien)

    def _check_alien_bottom(self):
        """ Check aliens for hit bottom screen and new game with lost ship health. """
        screen_rect = self.screen.get_rect()
        for aliens in self.aliens.sprites():
            if aliens.rect.bottom >= screen_rect.bottom:
                # Treat this the same as if the ship got hit.
                self._ship_hit()
                break

    def run_game(self):
        ''' Run game '''
        while True:
            # Check event
            self._check_event()

            if self.stats.game_active:
                # Ship position update
                self.ship.update()
                # Update position of bullets and remove extra bullets
                self._update_bullets()
                # Update position of fleet aliens
                self._update_aliens()

            # Update screen
            self._update_screen()

    def _update_aliens(self):
        """ Update position of aliens """
        self._check_fleet_edges()
        self.aliens.update()

        # Look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Look for alines hitting the bottom of the screen.
        self._check_alien_bottom()

    def _update_bullets(self):
        """ Update position of bullets and Get rid of bullets to remove """
        # Set update position fo bullets
        self.bullets.update()
        # Get rid of bullets that have desappeared
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        # Check bullet and alien for collisions and create if fleet is empty
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """ Checking bullets and aliens for collisions
            If aliens is empty, fleet aliens is created again. """
        # Check collisions of bullets and alien, then rid this
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        # Remove rest bullets and create another fleet aliens
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # Increase level.
            self.stats.level += 1
            self.sb.prep_level()

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
            # Check mouse click
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """ Check mouse click to play button for play game. """
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Reset the game settings
            self.settings.initialize_dynamic_settings()

            # Reset the game staticties
            self.stats.reset_stats()
            self.stats.game_active = True

            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            # Get rid of any remaining alines and bullets
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()

            # Hide cursor mouse in active game
            pygame.mouse.set_visible(False)

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
        # Draw alien on screen
        self.aliens.draw(self.screen)

        # Draw the socore information.
        self.sb.show_score()

        # Check inactive state and then show button play
        if not self.stats.game_active:
            self.play_button.draw_button()

        # Show screen object in loop
        pygame.display.flip()


# Main of program start
if __name__ == '__main__':
    # Create object
    ai = AlienInvasion()
    ai.run_game()
