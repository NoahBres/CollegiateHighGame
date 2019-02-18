import pygame
from pygame import locals, Vector2

# from .state import State
from CollegiateHighGame.states.state import State
from CollegiateHighGame.entities.player import Player
from CollegiateHighGame.entities.starfield import Starfield
from .player_view import PlayerView

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
        }

        self.player2.key_mapping = {
            "up": locals.K_UP,
            "down": locals.K_DOWN,
            "left": locals.K_LEFT,
            "right": locals.K_RIGHT,
        }

        player1_view_coords = (0, 0)
        player2_view_coords = (0, 0)

        self.player1_view = PlayerView(
            surface=self.game.screen,
            dimensions=player_view1_dimensions,
            coords=player1_view_coords,
            player=self.player1,
            game=self,
            padding=(130, 130),
        )
        self.player2_view = PlayerView(
            surface=self.game.screen,
            dimensions=player_view2_dimensions,
            coords=player2_view_coords,
            player=self.player2,
            game=self,
            padding=(130, 130),
        )

        self.player1.world_pos = Vector2(self.player1_view.coords.center)
        self.player2.world_pos = Vector2(self.player2_view.coords.center)

        self.world_state = WorldState()
        self.world_state.entities[self.player1] = self.player1
        self.world_state.entities[self.player2] = self.player2

        self.starfield = Starfield([self.player1_view, self.player2_view])

    def poll_events(self, events):
        self.player1.poll_events(events)
        self.player2.poll_events(events)

    def update(self):
        # self.player1.apply_force((0.01, 0.01))
        # self.player1.angle += 10

        self.player1.update()
        self.player2.update()

        self.starfield.update()

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


# State of the world. Not a "state" of the program
class WorldState:
    def __init__(self):
        self.width = 10000
        self.height = 10000

        self.entities = {}
