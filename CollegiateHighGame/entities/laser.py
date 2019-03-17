import os

import pygame

from pygame.math import Vector2

from .entity import Entity


class Laser(pygame.sprite.Sprite, Entity):
    def __init__(self, x, y, angle, speed, sprite_name, game, source):
        pygame.sprite.Sprite.__init__(self)
        Entity.__init__(self)

        base_path = os.path.dirname(__file__)
        base_path = os.path.abspath(os.path.join(base_path, os.path.pardir))
        image_path = os.path.join(base_path, "assets", "lasers", f"{sprite_name}.png")

        self.image = pygame.image.load(image_path).convert_alpha()
        scale = 0.8
        size = self.image.get_size()
        scaled_dimen = ((int(size[0] * scale)), int(size[1] * scale))
        self.image = pygame.transform.smoothscale(self.image, scaled_dimen)

        self.orig_rect = self.image.get_rect()

        self.image = pygame.transform.rotate(self.image, angle)
        # self.image = pygame.transform.rotozoom(self.image, angle, self.scale)

        self.rect = self.image.get_rect()

        self.world_pos = Vector2(x, y)
        self.angle = angle

        self.bound_x = game.world_state.width
        self.bound_y = game.world_state.height
        self.game = game
        self.game.world_state.entities[self] = self
        self.game.world_state.entities_map.add(self, self.world_pos)

        self.translation_vector = Vector2(0, 1).rotate(180 - angle)
        self.translation_vector.scale_to_length(speed)

        self.source = source

    def update(self, delta_time):
        last_pos = Vector2(self.world_pos)
        self.world_pos += (self.translation_vector / 10) * delta_time

        self.game.world_state.entities_map.update(self, last_pos, self.world_pos)

        if (
            self.world_pos.x < 0
            or self.world_pos.x > self.bound_x
            or self.world_pos.y < 0
            or self.world_pos.y > self.bound_y
        ):
            print(self.rect, self.world_pos)
            self.game.world_state.entities_map.delete(self, self.world_pos)
            del self.game.world_state.entities[self]

    def draw(self, surface, coords=None):
        rect = self.rect.copy()
        if coords is not None:
            rect.center = coords

        surface.blit(self.image, rect)
