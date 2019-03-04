import os

import pygame

from pygame.math import Vector2

from .entity import Entity


class Laser(pygame.sprite.Sprite, Entity):
    def __init__(self, x, y, angle, speed, sprite_name, game):
        pygame.sprite.Sprite.__init__(self)
        Entity.__init__(self)

        base_path = os.path.dirname(__file__)
        base_path = os.path.abspath(os.path.join(base_path, os.path.pardir))
        image_path = os.path.join(base_path, "assets", "lasers", f"{sprite_name}.png")

        self.image = pygame.image.load(image_path).convert_alpha()
        self.scale = 0.8
        self.image = pygame.transform.rotozoom(self.image, angle, self.scale)

        self.rect = self.image.get_rect()

        self.world_pos = Vector2(x, y)
        self.angle = angle

        game.world_state.entities[self] = self

        self.translation_vector = Vector2(0, 1).rotate(180 - angle)
        self.translation_vector.scale_to_length(speed)

        print(angle)

    def update(self):
        self.world_pos += self.translation_vector

    def draw(self, surface, coords=None):
        rect = self.rect.copy()
        if coords is not None:
            rect.center = coords

        surface.blit(self.image, rect)
