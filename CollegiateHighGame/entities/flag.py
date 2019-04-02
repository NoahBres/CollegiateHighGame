import os

import pygame
from pygame.math import Vector2

from .entity import Entity
from .player_base import PlayerBase


class Flag(pygame.sprite.Sprite, Entity):
    def __init__(self, x, y, sprite_name, game):
        pygame.sprite.Sprite.__init__(self)
        Entity.__init__(self)

        base_path = os.path.dirname(__file__)
        base_path = os.path.abspath(os.path.join(base_path, os.path.pardir))
        image_path = os.path.join(base_path, "assets", "entities", f"{sprite_name}.png")

        self.image = pygame.image.load(image_path).convert_alpha()
        scale = 0.5
        size = self.image.get_size()
        scaled_dimen = ((int(size[0] * scale)), int(size[1] * scale))
        self.image = pygame.transform.smoothscale(self.image, scaled_dimen)

        self.orig_rect = self.image.get_rect()
        self.rect = self.image.get_rect()

        self.world_pos = Vector2(x, y)
        self.angle = 0

        self.tethered = None

        self.game = game
        self.game.add_entity(self)

        self.draw_level = 1

    def update(self, delta_time):
        pass

    def draw(self, surface, coords=None):
        rect = self.rect.copy()
        if coords is not None:
            rect.center = coords

        surface.blit(self.image, rect)

    def tether(self, base):
        self.tethered = base
        base.tether(self)

        return self

    def untether(self, base):
        self.tethered = None
        base.untether(self)

        return self
