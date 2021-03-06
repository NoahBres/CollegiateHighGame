import pygame
from pygame import locals, Vector2

from random import randint
from time import time

# from .state import State
from CollegiateHighGame.states.state import State

from CollegiateHighGame.entities.player import Player
from CollegiateHighGame.entities.laser import Laser
from CollegiateHighGame.entities.player_base import PlayerBase
from CollegiateHighGame.entities.flag import Flag
from CollegiateHighGame.entities.starfield import Starfield
from CollegiateHighGame.entities.health_pill import HealthPill

from CollegiateHighGame.util.hash_map import HashMap
from .player_view import PlayerView
from .player_health import PlayerHealth
from .shot_count import ShotCount
from .speed_ui import SpeedUI

from .capture_ui import CaptureUI

white = (255, 255, 255)


class GameState(State):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.background = (29, 25, 35)
        self.divider_width = 4

        player_view1_dimensions = pygame.Rect(
            0, 0, (int(self.game.width / 2)), int(self.game.height)
        )
        player_view2_dimensions = pygame.Rect(
            self.game.width / 2, 0, (int(self.game.width / 2)), int(self.game.height)
        )

        player1_health_ui = PlayerHealth(
            (10, player_view1_dimensions.height - 10), 3, 100, "red"
        )
        player2_health_ui = PlayerHealth(
            (10, player_view2_dimensions.height - 10), 3, 100, "blue"
        )

        player1_shot_count_ui = ShotCount((10, player_view1_dimensions.height - 40), 8)
        player2_shot_count_ui = ShotCount((10, player_view2_dimensions.height - 40), 8)

        player1_speed_ui = SpeedUI(
            (20, player_view1_dimensions.height - 90), (10, 15), 1
        )
        player2_speed_ui = SpeedUI(
            (20, player_view2_dimensions.height - 90), (10, 15), 1
        )

        player1_capture_ui = CaptureUI(
            (20, player_view1_dimensions.height - 75), "spaceBuilding_015", 0
        )
        player2_capture_ui = CaptureUI(
            (20, player_view2_dimensions.height - 75), "spaceBuilding_014", 0
        )

        self.player1 = Player(
            player_view1_dimensions.width / 2,
            player_view1_dimensions.height / 2,
            "playerShip1_red",
            self.game.player1_joystick,
            self,
        )
        self.player2 = Player(
            player_view2_dimensions.width / 2,
            player_view2_dimensions.height / 2,
            "playerShip1_blue",
            self.game.player2_joystick,
            self,
        )

        self.player1.key_mapping["up"] = locals.K_w
        self.player1.key_mapping["down"] = locals.K_s
        self.player1.key_mapping["left"] = locals.K_a
        self.player1.key_mapping["right"] = locals.K_d
        self.player1.key_mapping["shoot"] = locals.K_SPACE
        self.player1.key_mapping["speed"] = locals.K_c

        self.player2.key_mapping["up"] = locals.K_UP
        self.player2.key_mapping["down"] = locals.K_DOWN
        self.player2.key_mapping["left"] = locals.K_LEFT
        self.player2.key_mapping["right"] = locals.K_RIGHT
        self.player2.key_mapping["shoot"] = locals.K_RSHIFT
        self.player2.key_mapping["speed"] = locals.K_SLASH

        # World State
        self.width = 6000
        self.height = 6000

        self.entities = {}
        # self.entities_spatial =
        self.cell_size = 100
        self.entities_map = HashMap(self.cell_size)

        player1_view_coords = (0, self.height / 2 - player_view1_dimensions.height / 2)
        player2_view_coords = (
            self.width - player_view2_dimensions.width,
            self.height / 2 - player_view2_dimensions.height / 2,
        )

        self.base1 = PlayerBase(
            player1_view_coords[0] + player_view1_dimensions.width / 2 - 200,
            player1_view_coords[1] + player_view1_dimensions.height / 2,
            self.player1,
            self.player2,
            self,
        )

        self.base2 = PlayerBase(
            player2_view_coords[0] + player_view2_dimensions.width / 2 + 200,
            player2_view_coords[1] + player_view2_dimensions.height / 2,
            self.player2,
            self.player1,
            self,
        )

        self.player1_view = PlayerView(
            surface=self.game.screen,
            dimensions=player_view1_dimensions,
            coords=player1_view_coords,
            player=self.player1,
            health_ui=player1_health_ui,
            shot_count_ui=player1_shot_count_ui,
            speed_ui=player1_speed_ui,
            capture_ui=player1_capture_ui,
            game=self,
            padding=(130, 130),
        )
        self.player2_view = PlayerView(
            surface=self.game.screen,
            dimensions=player_view2_dimensions,
            coords=player2_view_coords,
            player=self.player2,
            health_ui=player2_health_ui,
            shot_count_ui=player2_shot_count_ui,
            speed_ui=player2_speed_ui,
            capture_ui=player2_capture_ui,
            game=self,
            padding=(130, 130),
        )

        self.player1.world_pos = Vector2(self.player1_view.coords.center)
        self.player2.world_pos = Vector2(self.player2_view.coords.center)

        self.add_entity(self.player1)
        self.add_entity(self.player2)

        self.add_entity(self.base1)
        self.add_entity(self.base2)

        self.flag1 = Flag(
            self.base1.world_pos.x + self.base1.radius * 1.2,
            self.base1.world_pos.y + self.base1.radius * 1.2,
            "spaceBuilding_014",
            self.player1,
            self.player2,
            self.base1,
            self,
        ).tether(self.base1)
        self.add_entity(self.flag1)

        self.flag2 = Flag(
            self.base2.world_pos.x - self.base2.radius * 1.2,
            self.base2.world_pos.y + self.base2.radius * 1.2,
            "spaceBuilding_015",
            self.player2,
            self.player1,
            self.base2,
            self,
        ).tether(self.base2)
        self.add_entity(self.flag2)

        self.starfield = Starfield([self.player1_view, self.player2_view])
        self.starfield.prefill(10000, self.width, self.height)

        self.player1_flags = 0
        self.player2_flags = 0

        self.healthpill_last_spawn = 0
        self.healthpill_min_spawn_time = 10
        self.healthpill_spawn_time = randint(0, 10)

        # Spawn a bunch of health pills
        for i in range(randint(20, 30)):
            pill = HealthPill(randint(0, self.width), randint(0, self.height), self)
            self.add_entity(pill)

    def poll_events(self, events):
        self.player1.poll_events(events)
        self.player2.poll_events(events)

    def update(self, delta_time):
        for ent in list(self.entities):
            if not ent.depose:
                ent.update(delta_time)

            if isinstance(ent, Player):
                for item in self.entities_map.query_point(ent.world_pos):
                    if item is not ent and (
                        (isinstance(item, Laser)) or isinstance(item, HealthPill)
                    ):
                        ent.collide(item)

        if (
            time() - self.healthpill_last_spawn
            > self.healthpill_min_spawn_time + self.healthpill_spawn_time
        ):
            pill = HealthPill(randint(0, self.width), randint(0, self.height), self)
            self.add_entity(pill)
            self.healthpill_last_spawn = time()
            self.healthpill_spawn_time = randint(0, 10)
            print("spawn")

        self.starfield.update(delta_time)

    def draw(self, screen):
        screen.fill(self.background)

        self.starfield.draw()

        self.player1_view.draw()
        self.player2_view.draw()

        divider = pygame.Rect(
            self.game.center_width - self.divider_width / 2,
            0,
            self.divider_width,
            self.game.height,
        )
        screen.fill(white, divider)

    def add_entity(self, entity):
        self.entities[entity] = entity
        self.entities_map.add(entity, entity.world_pos)

    def remove_entity(self, entity):
        self.entities_map.delete(entity, entity.world_pos)
        try:
            del self.entities[entity]
        except Exception:
            pass

    def player_death(self, player):
        player.respawn()

        # if player is self.player1:
        #     print("player 1 died")
        # elif player is self.player2:
        #     print("player 2 died")

    def flag_capture(self, player):
        if player is self.player1:
            self.player1_flags += 1
        elif player is self.player2:
            self.player2_flags += 1

        if self.player1_flags == 3:
            print("player 1 wins")
        elif self.player2_flags == 3:
            print("player 2 wins")
