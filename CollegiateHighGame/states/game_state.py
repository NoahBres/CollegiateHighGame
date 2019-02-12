import pygame
from pygame import locals

from .state import State


class GameState(State):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.background = (29, 25, 35)

    def draw(self, screen):
        screen.fill(self.background)
