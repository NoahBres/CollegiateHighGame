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

        self.player1_view = self.game.screen.subsurface(
            player_view1_dimensions
        )  # pygame.Surface(player_view_dimensions)
        self.player1_view.fill((0, 255, 0))
        self.player1_view.set_colorkey((0, 255, 0))

        self.player2_view = self.game.screen.subsurface(
            player_view2_dimensions
        )  # pygame.Surface(player_view_dimensions)
        self.player2_view.fill((0, 255, 0))
        self.player2_view.set_colorkey((0, 255, 0))

        self.player1 = Player("playerShip1_red", self.player1_view)
        self.player2 = Player("playerShip1_blue", self.player2_view)

        self.bounce = 1

    def update(self):
        self.player1.angle += 10
        if self.player1.rect.x > self.game.center_width:
            self.bounce = -1
        elif self.player1.rect.x < 0:
            self.bounce = 1

        print(self.bounce)
        self.player1.rect.x += 5 * self.bounce

    def draw(self, screen):
        screen.fill(self.background)
        # self.player1_view.fill(self.background)
        # self.player2_view.fill(self.background)

        self.player1.draw()
        self.player2.draw()

        # screen.blit(self.player1_view, (0, 0))
        # screen.blit(self.player2_view, (self.game.center_width, 0))

        divider = pygame.Rect(
            self.game.center_width - self.divider_width / 2,
            0,
            self.divider_width,
            self.game.height,
        )
        screen.fill(white, divider)
