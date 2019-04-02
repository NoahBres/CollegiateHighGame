import os
from random import randint

import pygame
from pygame.math import Vector2

from .entity import Entity
from .player_base_turret import PlayerBaseTurret


class PlayerBase(pygame.sprite.Sprite, Entity):
    def __init__(self, x, y, owner, enemy, game):
        pygame.sprite.Sprite.__init__(self)
        Entity.__init__(self)

        base_path = os.path.dirname(__file__)
        base_path = os.path.abspath(os.path.join(base_path, os.path.pardir))

        meteor_path = os.path.join(
            base_path, "assets", "meteors", f"spaceMeteors_00{randint(1, 4)}.png"
        )

        self.orig_meteor_image = pygame.image.load(meteor_path).convert_alpha()
        self.meteor_image = self.orig_meteor_image.copy()
        # meteor_scale = 1.2
        # meteor_size = self.meteor_image.get_size()
        # meteor_scaled_dimen = (
        #     (int(meteor_size[0] * meteor_scale)),
        #     int(meteor_size[1] * meteor_scale),
        # )
        # self.meteor_image = pygame.transform.smoothscale(
        #     self.meteor_image, meteor_scaled_dimen
        # )

        self.orig_rect = self.meteor_image.get_rect()
        self.rect = self.meteor_image.get_rect()

        self.radius = self.orig_rect.width / 2 * 0.95

        self.world_pos = Vector2(x, y)
        self.angle = 0

        self.turret = PlayerBaseTurret(x, y, self, game)
        game.add_entity(self.turret)

        self.force = Vector2(randint(-10, 10) / 80, randint(-10, 10) / 80)
        # self.force = Vector2(-1, 0)
        self.rotation = randint(-10, 10) / 60

        self.game = game

        self.owner = owner
        self.enemy = enemy

        self.tethered = None
        self.tether_obj = None

        self.draw_level = 3

    def update(self, delta_time):
        # Drift
        # if (
        #     distance((self.world_pos.x, self.world_pos.y), (0, self.world_pos.y))
        #     <= self.radius
        # ):
        #     self.force.x = abs(self.force.x)
        if self.world_pos.x - self.rect.width / 2 <= 0:
            self.force.x = abs(self.force.x)
        elif self.world_pos.x + self.rect.width / 2 >= self.game.width:
            self.force.x = -abs(self.force.x)

        if self.world_pos.y - self.rect.height / 2 <= 0:
            self.force.y = abs(self.force.y)
        elif self.world_pos.y + self.rect.height / 2 >= self.game.height:
            self.force.y = -abs(self.force.y)

        self.world_pos += self.force / 16 * delta_time
        self.turret.world_pos = self.world_pos

        # Rotation
        self.angle += self.rotation / 16 * delta_time
        self.meteor_image = pygame.transform.rotate(self.orig_meteor_image, self.angle)
        self.rect = self.meteor_image.get_rect(center=self.rect.center)

        self.turret.set_foundation_angle(self.angle)

        if self.world_pos.distance_to(self.enemy.world_pos) < 600:
            self.turret.target(self.enemy.world_pos)
        else:
            self.turret.untarget()

        # self.turret.update(delta_time)

    def draw(self, surface, coords=None):
        rect = self.rect.copy()
        if coords is not None:
            rect.center = coords

        surface.blit(self.meteor_image, rect)
        # self.turret.draw(surface, rect.center)
        # pygame.draw.circle(surface, (255, 255, 255), rect.center, int(self.radius), 1)

    def tether(self, flag, tether_obj):
        self.tethered = flag
        self.tether_obj = tether_obj

        return self

    def untether(self, flag):
        self.tethered = None
        self.game.remove_entity(self.tether_obj)
        self.tether_obj = None

        return self
