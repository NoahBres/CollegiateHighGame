import pygame
from pygame.math import Vector2

from .mini_map import MiniMap

DEBUG_PADDING_LINE = False


class PlayerView:
    def __init__(
        self,
        surface,
        dimensions,
        coords,
        player,
        health_ui,
        shot_count_ui,
        speed_ui,
        capture_ui,
        game,
        padding,
    ):
        self.dimensions = dimensions
        self.coords = pygame.Rect(
            coords[0], coords[1], dimensions.width, dimensions.height
        )
        self.surface = surface.subsurface(dimensions)
        # Make view transparent
        self.surface.fill((0, 255, 0))
        self.surface.set_colorkey((0, 255, 0))

        self.player = player
        self.game = game

        self.padding = padding
        self.padding_rect = pygame.Rect(
            padding[0],
            padding[1],
            dimensions.width - padding[0] * 2,
            dimensions.height - padding[1] * 2,
        )

        self.player.view = self
        self.health_ui = health_ui
        self.shot_count_ui = shot_count_ui
        self.speed_ui = speed_ui
        self.capture_ui = capture_ui

        mini_map_dimen = (150, 150)
        mini_map_padding = (10, 10)
        self.mini_map = MiniMap(
            dimensions.width - mini_map_dimen[0] - mini_map_padding[0],
            mini_map_padding[1],
            mini_map_dimen[0],
            mini_map_dimen[1],
            self,
        )

    def draw(self):
        for entity in sorted(
            list(self.game.entities.values()), key=lambda x: x.draw_level, reverse=True
        ):
            if entity != self.player:
                offset_coords = Vector2(entity.world_pos) - Vector2(
                    self.coords.x, self.coords.y
                )
                entity.draw(self.surface, offset_coords)

        self.player.draw(self.surface)

        coords_font = pygame.font.Font(None, 25)
        coords_text = coords_font.render(
            f"{self.coords.centerx}, {self.coords.centery}", True, (255, 255, 255)
        )
        self.surface.blit(
            coords_text,
            (
                self.surface.get_width() - coords_text.get_width() - 15,
                self.surface.get_height() - coords_text.get_height() - 20,
            ),
        )

        self.mini_map.draw(self.surface)
        self.health_ui.draw(self.surface)
        self.shot_count_ui.draw(self.surface)
        self.speed_ui.draw(self.surface)
        self.capture_ui.draw(self.surface)

        if DEBUG_PADDING_LINE:
            line_points = [
                self.padding_rect.topleft,
                self.padding_rect.topright,
                self.padding_rect.bottomright,
                self.padding_rect.bottomleft,
                self.padding_rect.topleft,
            ]
            pygame.draw.lines(self.surface, (255, 255, 255), True, line_points, 1)
