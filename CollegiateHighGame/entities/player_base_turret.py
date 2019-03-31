import os
from math import degrees, atan2

import pygame
from pygame.math import Vector2

from .entity import Entity


class PlayerBaseTurret(pygame.sprite.Sprite, Entity):
    def __init__(self, x, y, base, game):
        pygame.sprite.Sprite.__init__(self)
        Entity.__init__(self)

        base_path = os.path.dirname(__file__)
        base_path = os.path.abspath(os.path.join(base_path, os.path.pardir))

        foundation_path = os.path.join(
            base_path, "assets", "entities", "spaceBuilding_018.png"
        )
        turret_path = os.path.join(
            base_path, "assets", "entities", "spaceBuilding_022.png"
        )

        self.orig_foundation_image = pygame.image.load(foundation_path).convert_alpha()
        self.foundation_image = self.orig_foundation_image.copy()
        self.orig_rect = self.foundation_image.get_rect()

        self.foundation_angle = 45
        self.foundation_image = pygame.transform.rotate(
            self.foundation_image, self.foundation_angle
        )
        self.rect = self.foundation_image.get_rect()

        self.orig_turret_image = pygame.image.load(turret_path).convert_alpha()
        self.turret_image = self.orig_turret_image.copy()
        self.orig_turret_rect = self.turret_image.get_rect()
        self.turret_rect = self.turret_image.get_rect()

        self.world_pos = Vector2(x, y)
        self.turret_angle = 0
        self.turret_target_angle = 0

        self.last_turret_target_angle = 0

        self.turret_speed = 1

        self.base = base
        self.game = game

    def update(self, delta_time):
        if self.turret_angle * 2 > self.turret_target_angle * 2:
            self.turret_angle -= self.turret_speed / 16 * delta_time
            self.set_turret_angle(self.turret_angle)
        elif self.turret_angle * 2 < self.turret_target_angle * 2:
            self.turret_angle += self.turret_speed / 16 * delta_time
            self.set_turret_angle(self.turret_angle)
        # self.turret_angle

    def draw(self, surface, coords=None):
        rect = self.rect.copy()
        turret_rect = self.turret_rect.copy()
        if coords is not None:
            rect.center = coords
            turret_rect.center = coords

        surface.blit(self.foundation_image, rect)
        surface.blit(self.turret_image, turret_rect)

    def set_foundation_angle(self, angle):
        self.foundation_angle = angle

        self.foundation_image = pygame.transform.rotate(
            self.orig_foundation_image, self.foundation_angle
        )
        self.rect = self.foundation_image.get_rect(center=self.rect.center)

    def set_turret_angle(self, angle):
        self.turret_angle = angle

        self.turret_image = pygame.transform.rotate(
            self.orig_turret_image, self.turret_angle
        )
        self.turret_rect = self.turret_image.get_rect(center=self.turret_rect.center)

    def target(self, point):
        # self.set_turret_angle(90)
        # self.turret_target_angle = degrees(self.world_pos.angle_to(point))
        # difference = point - self.world_pos
        # self.turret_target_angle = 270 - degrees(atan2(difference.y, difference.x))
        difference = self.world_pos - point
        self.turret_target_angle = 90 - degrees(atan2(difference.y, difference.x))

        # Values are arbitrarily set. Should probably make them variables
        if self.turret_target_angle > 250 and self.last_turret_target_angle < -70:
            self.turret_angle += 360
        elif self.turret_target_angle < -70 and self.last_turret_target_angle > 250:
            self.turret_angle -= 360
            # self.turret_target_angle = -90 - (270 - self.turret_target_angle)

        self.last_turret_target_angle = self.turret_target_angle
