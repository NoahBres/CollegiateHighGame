import os
from math import cos, sin, atan2, radians, degrees
from time import time

import pygame
from pygame.math import Vector2

from .entity import Entity
from .laser import Laser
from CollegiateHighGame.util.utils import remap, limit_vec, collide_circle_rect

DEBUG_TARGET = True
DEBUG_SPEEDY = True


class Player(pygame.sprite.Sprite, Entity):
    def __init__(self, x, y, sprite_name, game):
        # super().__init__()
        pygame.sprite.Sprite.__init__(self)
        Entity.__init__(self)

        self.game = game
        self.view = None

        # -- Begin Load image -- #
        base_path = os.path.dirname(__file__)
        base_path = os.path.abspath(os.path.join(base_path, os.path.pardir))
        image_path = os.path.join(base_path, "assets", "ships", f"{sprite_name}.png")

        laser_sound_path = os.path.join(base_path, "assets", "sound", "sfx_laser1.ogg")
        ping_sound_path = os.path.join(base_path, "assets", "sound", "tone1.wav")

        fire_path = os.path.join(base_path, "assets", "effects", "fire17.png")

        damage_path = [
            os.path.join(base_path, "assets", "effects", "playerShip1_damage1.png"),
            os.path.join(base_path, "assets", "effects", "playerShip1_damage2.png"),
            os.path.join(base_path, "assets", "effects", "playerShip1_damage3.png"),
        ]

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

        self.orig_rect = self.image.get_rect()

        fire_scale = 0.6
        self.fire_img = pygame.image.load(fire_path).convert_alpha()
        self.fire_img = pygame.transform.smoothscale(
            self.fire_img,
            (
                int(self.fire_img.get_width() * fire_scale),
                int(self.fire_img.get_height() * fire_scale),
            ),
        )

        self.damage_img = [
            pygame.image.load(img).convert_alpha() for img in damage_path
        ]
        self.damage_img = [
            pygame.transform.smoothscale(img, scaled_dimensions)
            for img in self.damage_img
        ]

        self.curr_damage_img = None

        self.laser_sound = pygame.mixer.Sound(laser_sound_path)
        self.ping_sound = pygame.mixer.Sound(ping_sound_path)
        # -- End Load Assets -- #

        self.rect.center = (x, y)

        self.draw_level = 0

        # To fix circular dependency between health and angle
        self.__health = 100
        self.__angle = 0

        self.health = 100
        self.current_damage_indicator = -1

        self.lives = 3

        self.pressing_speed = False

        self.tethered_speed = 4
        self.normal_speed = 7
        self.super_speed = 18

        self.speed_max_percent = 100
        self.speed_percent = self.speed_max_percent
        self.speed_refresh_rate = 1

        self.max_speed = self.normal_speed
        self.max_steer = 0.2
        self.deceleration_rate = 0.97

        self.angle = 0

        self.position = Vector2(self.rect.center)
        self.velocity = Vector2(0, 0)
        self.acceleration = Vector2(0, 0)

        self.force = (
            self.velocity
        )  # provides a link to from force to velocity to keep compatability with flag's logic

        self.target = self.rect.copy()
        self.target_radius = 0
        self.target_max_radius = self.rect.width * 1.3
        self.target_angle = -90

        self.key_mapping = {
            "up": None,
            "down": None,
            "left": None,
            "right": None,
            "shoot": None,
            "speed": None,
        }

        self.shot_max = 8
        self.shot_count = self.shot_max
        self.last_recharge_time = 0
        self.shot_recharge_time = 800  # milliseconds

        self.tethered = None
        self.tether_obj = None

        self.radius = self.orig_rect.width / 2

    def update(self, delta_time):
        # Super speed
        if self.pressing_speed and self.speed_percent > 0:
            self.max_speed = self.super_speed
            if not DEBUG_SPEEDY:
                self.speed_percent -= 1
        else:
            self.max_speed = self.normal_speed

            if self.speed_percent < 100:
                self.speed_percent += 0.3

        self.view.speed_ui.set_percent(self.speed_percent / 10)

        # Movement
        self.velocity += self.acceleration
        limit_vec(self.velocity, self.max_speed)

        if self.acceleration.length() == 0 and self.velocity.length() > 0.00001:
            self.velocity.scale_to_length(self.velocity.length() * 0.97)

        # self.view.coords.move(self.velocity)
        # self.view.coords.x += self.velocity.x
        # self.view.coords.y += self.velocity.y
        # self.game.entities[self].world_pos += self.velocity
        # self.position += self.velocity
        # self.game.entities[self].world_pos = self.position

        # if (self.position.x <= self.view.padding_rect.x + self.rect.width) or (
        #     self.position.x + self.rect.width / 2
        #     >= self.view.padding_rect.x + self.view.padding_rect.width
        # ):
        #     self.view.coords.x += self.velocity.x
        #     self.position.x -= self.velocity.x

        # if (self.position.y <= self.view.padding_rect.y) or (
        #     self.position.y + self.rect.height
        #     >= self.view.padding_rect.y + self.view.padding_rect.height
        # ):
        #     self.view.coords.y += self.velocity.y
        #     self.position.y -= self.velocity.y

        # center player in frame movement
        last_pos = Vector2(self.world_pos)

        self.world_pos += (self.velocity / 10) * delta_time
        self.view.coords.center = self.world_pos
        # self.view.coords += self.velocity

        if last_pos != self.world_pos:
            self.game.entities_map.update(self, last_pos, self.world_pos)

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

        # Shoot limiter
        if (
            self.shot_count < self.shot_max
            and time() * 1000 - self.last_recharge_time > self.shot_recharge_time
        ):
            self.shot_count += 1
            self.last_recharge_time = time() * 1000
            self.view.shot_count_ui.set_count(self.shot_count)

    def poll_events(self, events):
        keys = pygame.key.get_pressed()

        if keys[self.key_mapping["up"]]:
            self.target_radius = 1
            if keys[self.key_mapping["right"]]:
                self.target_angle = 315
            elif keys[self.key_mapping["left"]]:
                self.target_angle = 225
            else:
                self.target_angle = 270
        elif keys[self.key_mapping["down"]]:
            self.target_radius = 1
            if keys[self.key_mapping["right"]]:
                self.target_angle = 45
            elif keys[self.key_mapping["left"]]:
                self.target_angle = 135
            else:
                self.target_angle = 90
        elif keys[self.key_mapping["right"]]:
            self.target_radius = 1
            self.target_angle = 0
        elif keys[self.key_mapping["left"]]:
            self.target_radius = 1
            self.target_angle = 180
        else:
            self.target_radius = 0

        if keys[self.key_mapping["speed"]]:
            self.pressing_speed = True
        else:
            self.pressing_speed = False

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == self.key_mapping["shoot"]:
                    self.shoot()

    def draw(self, surface, coords=None):
        rect = self.rect.copy()
        if coords is not None:
            rect.center = coords

        # surface.blit(self.fire_img, rect)

        surface.blit(self.image, rect)
        if self.current_damage_indicator != -1:
            surface.blit(self.curr_damage_img, rect)

        # Debug Target
        if coords is None and DEBUG_TARGET:
            pygame.draw.circle(
                surface,
                (255, 255, 255),
                self.rect.center,
                int(self.target_max_radius),
                1,
            )

            if self.target.center != self.rect.center:
                target_size = 3
                pygame.draw.circle(
                    surface, (0, 255, 0), self.target.center, target_size
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

        if self.current_damage_indicator != -1:
            self.curr_damage_img = pygame.transform.rotate(
                self.damage_img[self.current_damage_indicator], self.angle
            )

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

        if self.current_damage_indicator != -1:
            self.curr_damage_img = pygame.transform.rotate(
                self.damage_img[self.current_damage_indicator], self.angle
            )

    @property
    def health(self):
        return self.__health

    @health.setter
    def health(self, health):
        self.__health = health

        if self.health > 75:
            self.current_damage_indicator = -1
        elif self.health > 50:
            self.current_damage_indicator = 0
        elif self.health > 25:
            self.current_damage_indicator = 1
        else:
            self.current_damage_indicator = 2

        self.curr_damage_img = self.damage_img[self.current_damage_indicator]
        self.curr_damage_img = pygame.transform.rotate(
            self.damage_img[self.current_damage_indicator], self.angle
        )

        if self.view is not None:
            self.view.health_ui.set_health(self.health)

        if self.health < 0:
            self.game.player_death(self)
        print(self.health)

    def shoot(self):
        if self.shot_count <= 0:
            return

        self.shot_count -= 1
        self.last_recharge_time = time() * 1000
        self.view.shot_count_ui.set_count(self.shot_count)

        Laser(
            self.world_pos.x,
            self.world_pos.y,
            self.angle,
            10,
            "laserRed01",
            self.game,
            self.hash,
        )
        self.laser_sound.play()

    def collide(self, entity):
        if self.hash != entity.source and collide_circle_rect(
            {
                "x": self.world_pos.x,
                "y": self.world_pos.y,
                "radius": self.orig_rect.width,
            },
            {
                "x": entity.world_pos.x,
                "y": entity.world_pos.y,
                "width": entity.orig_rect.width,
                "height": entity.orig_rect.height,
                "angle": radians(entity.angle),
            },
        ):
            if entity.depose:
                self.game.remove_entity(entity)
                return

            entity.depose = True
            self.game.remove_entity(entity)

            self.health -= 10

            self.ping_sound.play()
        # print("-----------")
        # print(entity.orig_rect, self.orig_rect)
        # print(entity.angle, self.angle)
        # print(entity.world_pos, self.world_pos)
        # print(",,,,")
        # print(entity.rect, self.rect)

    def respawn(self):
        self.lives -= 1
        self.health = 100
        self.view.health_ui.set_lives(self.lives)

        # self.

    def tether(self, flag, tether_obj):
        self.tethered = flag
        self.tether_obj = tether_obj

        self.max_speed = self.tethered_speed

        return self

    def untether(self, flag):
        self.tethered = None
        self.game.remove_entity(self.tether_obj)
        self.tether_obj = None

        self.max_speed = self.normal_speed

        return self
