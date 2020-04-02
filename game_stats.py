
class GameStats:
    """ Track staticties for Alien Invasion """

    def __init__(self, ai_game):
        """ Initialization """
        self.settings = ai_game.settings
        self.reset_stats()
        # Flag game active
        self.game_active = True

    def reset_stats(self):
        """ Initialize staticties that can change during game. """
        self.ships_left = self.settings.ship_limit
