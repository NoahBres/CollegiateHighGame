import pygame
from pygame import locals, Vector2

# from .state import State
from CollegiateHighGame.states.state import State

from CollegiateHighGame.entities.player import Player
from CollegiateHighGame.entities.laser import Laser
from CollegiateHighGame.entities.player_base import PlayerBase
from CollegiateHighGame.entities.flag import Flag
from CollegiateHighGame.entities.starfield import Starfield

from CollegiateHighGame.util.hash_map import HashMap
from .player_view import PlayerView
from .player_health import PlayerHealth
from .shot_count import ShotCount

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

        self.player1 = Player(
            player_view1_dimensions.width / 2,
            player_view1_dimensions.height / 2,
            "playerShip1_red",
            self,
        )
        self.player2 = Player(
            player_view2_dimensions.width / 2,
            player_view2_dimensions.height / 2,
            "playerShip1_blue",
            self,
        )

        self.player1.key_mapping = {
            "up": locals.K_w,
            "down": locals.K_s,
            "left": locals.K_a,
            "right": locals.K_d,
            "shoot": locals.K_SPACE,
        }

        self.player2.key_mapping = {
            "up": locals.K_UP,
            "down": locals.K_DOWN,
            "left": locals.K_LEFT,
            "right": locals.K_RIGHT,
            "shoot": locals.K_RSHIFT,
        }

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
            self,
        ).tether(self.base1)
        self.add_entity(self.flag1)

        self.flag2 = Flag(
            self.base2.world_pos.x - self.base2.radius * 1.2,
            self.base2.world_pos.y + self.base2.radius * 1.2,
            "spaceBuilding_015",
            self,
        ).tether(self.base2)
        self.add_entity(self.flag2)

        self.starfield = Starfield([self.player1_view, self.player2_view])
        self.starfield.prefill(10000, self.width, self.height)

    def poll_events(self, events):
        self.player1.poll_events(events)
        self.player2.poll_events(events)

    def update(self, delta_time):
        for ent in list(self.entities):
            if not ent.depose:
                ent.update(delta_time)

            if isinstance(ent, Player):
                for item in self.entities_map.query_point(ent.world_pos):
                    if item is not ent and (isinstance(item, Laser)):
                        ent.collide(item)
        # for key, cell in list(self.entities_map.grid.items()):
        # for ent in cell:
        # ent.update(delta_time)

        # self.player1.update()
        # self.player2.update()

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

        if player is self.player1:
            print("player 1 died")
        elif player is self.player2:
            print("player 2 died")
