import pygame
from pygame import locals

from .state import State


white = (255, 255, 255)


class GameState(State):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.background = (29, 25, 35)
        self.divider_width = 4

    def draw(self, screen):
        screen.fill(self.background)

        divider = pygame.Rect(
            self.game.center_width - self.divider_width / 2,
            0,
            self.divider_width,
            self.game.height,
        )
        screen.fill(white, divider)
