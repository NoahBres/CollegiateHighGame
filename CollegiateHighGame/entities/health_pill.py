import os
from random import randint

import pygame
from pygame.math import Vector2

from .entity import Entity


class HealthPill(pygame.sprite.Sprite, Entity):
    def __init__(self, x, y, game):
        pygame.sprite.Sprite.__init__(self)
        Entity.__init__(self)

        base_path = os.path.dirname(__file__)
        base_path = os.path.abspath(os.path.join(base_path, os.path.pardir))

        image_path = os.path.join(base_path, "assets", "entities", "pill_green.png")

        self.orig_image = pygame.image.load(image_path).convert_alpha()
        self.image = self.orig_image.copy()

        self.orig_rect = self.orig_image.get_rect()
        self.rect = self.image.get_rect()

        self.radius = self.orig_rect.width / 2 * 0.95

        self.world_pos = Vector2(x, y)
        self.angle = 0

        self.force = Vector2(randint(-10, 10) / 80, randint(-10, 10) / 80)
        self.rotation = randint(-10, 10) / 60

        self.game = game

        self.draw_level = 4

    def update(self, delta_time):
        if self.world_pos.x - self.rect.width / 2 <= 0:
            self.force.x = abs(self.force.x)
        elif self.world_pos.x + self.rect.width / 2 >= self.game.width:
            self.force.x = -abs(self.force.x)

        if self.world_pos.y - self.rect.height / 2 <= 0:
            self.force.y = abs(self.force.y)
        elif self.world_pos.y + self.rect.height / 2 >= self.game.height:
            self.force.y = -abs(self.force.y)

        last_pos = Vector2(self.world_pos)

        self.world_pos += self.force / 16 * delta_time

        if last_pos != self.world_pos:
            self.game.entities_map.update(self, last_pos, self.world_pos)

        # Rotation
        self.angle += self.rotation / 16 * delta_time
        self.image = pygame.transform.rotate(self.orig_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def draw(self, surface, coords=None):
        rect = self.rect.copy()
        if coords is not None:
            rect.center = coords

        surface.blit(self.image, rect)
