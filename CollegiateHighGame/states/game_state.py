import pygame
from pygame import locals

from .state import State
from CollegiateHighGame.entities.player import Player

white = (255, 255, 255)


class GameState(State):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.background = (29, 25, 35)
        self.divider_width = 4

        player_view1_dimensions = pygame.Rect(
            0, 0, (int(self.game.width / 2)), int(self.game.height)
        )
        player_view2_dimensions = pygame.Rect(
            self.game.width / 2, 0, (int(self.game.width / 2)), int(self.game.height)
        )

        self.player1_view = self.game.screen.subsurface(player_view1_dimensions)
        self.player1_view.fill((0, 255, 0))
        self.player1_view.set_colorkey((0, 255, 0))

        self.player2_view = self.game.screen.subsurface(player_view2_dimensions)
        self.player2_view.fill((0, 255, 0))
        self.player2_view.set_colorkey((0, 255, 0))

        self.player1 = Player("playerShip1_red", self.player1_view)
        self.player2 = Player("playerShip1_blue", self.player2_view)

    def update(self):
        # self.player1.apply_force((0.01, 0.01))
        # self.player1.angle += 10
        self.player1.update()
        self.player2.update()

    def draw(self, screen):
        screen.fill(self.background)

        self.player1.draw()
        self.player2.draw()

        divider = pygame.Rect(
            self.game.center_width - self.divider_width / 2,
            0,
            self.divider_width,
            self.game.height,
        )
        screen.fill(white, divider)
