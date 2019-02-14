import os
from math import cos, sin, atan2, radians, degrees

import pygame

from pygame.math import Vector2
from CollegiateHighGame.util.utils import remap, limit_vec

DEBUG_TARGET = True


class Player(pygame.sprite.Sprite):
    def __init__(self, sprite_name, surface):
        super().__init__()

        # -- Load image -- #
        base_path = os.path.dirname(__file__)
        image_path = os.path.abspath(os.path.join(base_path, os.path.pardir))
        image_path = os.path.join(image_path, "assets", "ships", f"{sprite_name}.png")

        self.orig_image = pygame.image.load(image_path).convert_alpha()
        # self.image.set_colorkey((0, 0, 0))
        self.rect = self.orig_image.get_rect()

        size = self.orig_image.get_size()

        self.scale = 0.5

        scaled_dimensions = ((int(size[0] * self.scale)), int(size[1] * self.scale))
        self.scaled_image = pygame.transform.smoothscale(
            self.orig_image, scaled_dimensions
        )
        self.image = self.scaled_image
        self.rect = self.image.get_rect()
        # -- Load Image -- #

        self.surface = surface

        self.rect.center = (
            self.surface.get_rect().width / 2,
            self.surface.get_rect().height / 2,
        )

        self.max_speed = 9
        self.max_steer = 0.2
        self.deceleration_rate = 0.97

        self.angle = 0

        self.position = Vector2(self.rect.center)
        self.velocity = Vector2(0, 0)
        self.acceleration = Vector2(0, 0)

        self.target = self.rect.copy()
        self.target_radius = 0
        self.target_max_radius = self.rect.width * 1.3
        self.target_angle = -90

    def update(self):
        self.velocity += self.acceleration
        limit_vec(self.velocity, self.max_speed)

        if self.acceleration.length() == 0 and self.velocity.length() > 0.00001:

        self.position += self.velocity
        self.acceleration.x = 0
        self.acceleration.y = 0

        self.rect.center = self.position

        self.target.centerx = (
            cos(radians(self.target_angle))
            * (self.target_radius * self.target_max_radius)
            + self.rect.centerx
        )
        self.target.centery = (
            sin(radians(self.target_angle))
            * (self.target_radius * self.target_max_radius)
            + self.rect.centery
        )

        if self.target_radius > 0:
            self.arrive_target(Vector2(self.target.centerx, self.target.centery))
            self.angle = -degrees(atan2(self.velocity.y, self.velocity.x)) - 90

    def draw(self):
        self.surface.blit(self.image, self.rect)

        # Debug Target
        if DEBUG_TARGET:
            pygame.draw.circle(
                self.surface,
                (255, 255, 255),
                self.rect.center,
                int(self.target_max_radius),
                1,
            )

            target_size = 3
            pygame.draw.circle(
                self.surface, (0, 255, 0), self.target.center, target_size
            )

    def apply_force(self, force):
        self.acceleration += force

    def arrive_target(self, target):
        desired_pos = target - self.position
        desired_mag = desired_pos.length()

        # Scale with arbitrary damping within 100 pixels
        if desired_mag < 100:
            mapped = remap(desired_mag, 0, 100, 0, self.max_speed)
            desired_pos.scale_to_length(mapped)
        else:
            desired_mag.scale_to_length(self.max_speed)

        steer = desired_pos - self.velocity
        limit_vec(steer, self.max_steer)
        self.apply_force(steer)

    def set_angle(self, angle):
        self.angle = angle
        self.image = pygame.transform.rotate(self.scaled_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    @property
    def angle(self):
        return self.__angle

    @angle.setter
    def angle(self, angle):
        self.__angle = angle

        # orig_center = self.scaled_image.get_rect().center
        self.image = pygame.transform.rotate(self.scaled_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        # self.image.get_rect().center = orig_center
