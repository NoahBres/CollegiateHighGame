import os
from math import radians, degrees, atan2, cos, sin
from random import randint

import pygame
from pygame.math import Vector2

from .entity import Entity
from .tether import Tether

# from .player import Player
from .player_base import PlayerBase

from CollegiateHighGame.util.utils import collide_circle_rect


class Flag(pygame.sprite.Sprite, Entity):
    def __init__(self, x, y, sprite_name, owner, enemy, game):
        pygame.sprite.Sprite.__init__(self)
        Entity.__init__(self)

        base_path = os.path.dirname(__file__)
        base_path = os.path.abspath(os.path.join(base_path, os.path.pardir))
        image_path = os.path.join(base_path, "assets", "entities", f"{sprite_name}.png")

        self.orig_image = pygame.image.load(image_path).convert_alpha()
        scale = 0.5
        size = self.orig_image.get_size()
        scaled_dimen = ((int(size[0] * scale)), int(size[1] * scale))
        self.orig_image = pygame.transform.smoothscale(self.orig_image, scaled_dimen)
        self.image = self.orig_image.copy()

        self.orig_rect = self.orig_image.get_rect()
        self.rect = self.image.get_rect()

        self.world_pos = Vector2(x, y)
        self.angle = 0

        self.force = Vector2(0, 0)
        self.rotation = randint(-10, 10) / 60

        self.tethered = None
        self.tether_obj = None

        self.owner = owner
        self.enemy = enemy

        self.game = game
        self.game.add_entity(self)

        self.draw_level = 3

    def update(self, delta_time):
        if self.tethered is not None:
            distance_to_tethered = abs(
                self.world_pos.distance_to(self.tethered.world_pos)
            )
            if distance_to_tethered > self.tether_obj.max_length:
                # self.force = self.tethered.force

                difference = self.world_pos - self.enemy.world_pos
                angle = radians(180) - atan2(difference.y, difference.x)

                target_force = self.tethered.force.length()

                print(degrees(angle))

                self.force = Vector2(
                    cos(angle) * target_force, sin(angle) * target_force
                )
            elif (
                distance_to_tethered < self.tethered.radius + self.orig_rect.width / 2
                and collide_circle_rect(
                    {
                        "x": self.tethered.world_pos.x,
                        "y": self.tethered.world_pos.y,
                        "radius": self.tethered.radius * 2,
                    },
                    {
                        "x": self.world_pos.x,
                        "y": self.world_pos.y,
                        "width": self.orig_rect.width,
                        "height": self.orig_rect.height,
                        "angle": radians(180 - self.angle),
                    },
                )
            ):
                # print(f"----{self.hash}----")
                # print(degrees(self.world_pos.angle_to(self.tethered.world_pos)))
                # self.force.rotate(
                #     degrees(self.world_pos.angle_to(self.tethered.world_pos))
                #     - Vector2(0, 0).angle_to(self.world_pos)
                # )
                self.force = self.tethered.force * 1.2

            if isinstance(self.tethered, PlayerBase) and collide_circle_rect(
                {
                    "x": self.enemy.world_pos.x,
                    "y": self.enemy.world_pos.y,
                    "radius": self.enemy.orig_rect.width / 2,
                },
                {
                    "x": self.world_pos.x,
                    "y": self.world_pos.y,
                    "width": self.orig_rect.width,
                    "height": self.orig_rect.height,
                    "angle": radians(self.angle),
                },
            ):
                self.untether(self.tethered)
                self.tether(self.enemy)

        self.world_pos += self.force / 16 * delta_time

        if self.world_pos.x - self.rect.width / 2 <= 0:
            self.force.x = abs(self.force.x)
        elif self.world_pos.x + self.rect.width / 2 >= self.game.width:
            self.force.x = -abs(self.force.x)

        if self.world_pos.y - self.rect.height / 2 <= 0:
            self.force.y = abs(self.force.y)
        elif self.world_pos.y + self.rect.height / 2 >= self.game.height:
            self.force.y = -abs(self.force.y)

        self.angle += self.rotation / 16 * delta_time
        self.image = pygame.transform.rotate(self.orig_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def draw(self, surface, coords=None):
        rect = self.rect.copy()
        if coords is not None:
            rect.center = coords

        surface.blit(self.image, rect)

    def tether(self, base):
        self.tethered = base
        self.tether_obj = Tether(base, self, self.game)
        base.tether(self, self.tether_obj)

        # self.force = base.force

        return self

    def untether(self, base):
        # if self.tethered is None:
        # if base is None:
        #     return self

        base.untether(self)
        self.tethered = None
        self.tether_obj = None

        return self
