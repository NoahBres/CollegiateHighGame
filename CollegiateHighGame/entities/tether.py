import pygame
from pygame.math import Vector2

from .entity import Entity


class Tether(pygame.sprite.Sprite, Entity):
    def __init__(self, point1, point2, game):
        pygame.sprite.Sprite.__init__(self)
        Entity.__init__(self)

        self.point1 = point1
        self.point2 = point2

        self.rect = pygame.Rect(
            0,
            0,
            point1.world_pos.x - point2.world_pos.x,
            point1.world_pos.y - point2.world_pos.y,
        )

        self.world_pos = point1.world_pos

        self.game = game
        self.game.add_entity(self)

        self.draw_level = 2

    def update(self, delta_time):
        self.rect = pygame.Rect(
            0,
            0,
            self.point1.world_pos.x - self.point2.world_pos.x,
            self.point1.world_pos.y - self.point2.world_pos.y,
        )

    def draw(self, surface, coords=None):
        rect = self.rect.copy()
        if coords is not None:
            rect.bottomright = coords

        pygame.draw.line(surface, (20, 20, 20), rect.topleft, rect.bottomright, 2)
