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

        player_view_dimensions = ((int(self.game.width / 2)), int(self.game.height))

        self.player1_view = pygame.Surface(player_view_dimensions)
        self.player1_view.fill((0, 255, 0))
        self.player1_view.set_colorkey((0, 255, 0))

        self.player2_view = pygame.Surface(player_view_dimensions)
        self.player2_view.fill((0, 255, 0))
        self.player2_view.set_colorkey((0, 255, 0))

        self.player_group = pygame.sprite.Group()

        self.player1 = Player()
        self.player_group.add(self.player1)

    def update(self):
        pass

    def draw(self, screen):
        screen.fill(self.background)

        # self.player_group.draw(screen)
        self.player1_view.blit(self.player1.image, (800, 0))

        screen.blit(self.player1_view, (0, 0))
        screen.blit(self.player2_view, (self.game.center_width, 0))

        divider = pygame.Rect(
            self.game.center_width - self.divider_width / 2,
            0,
            self.divider_width,
            self.game.height,
        )
        screen.fill(white, divider)
