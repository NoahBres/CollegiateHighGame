from random import randrange
import time
import pygame
from pygame.math import Vector2

from .entity import Entity
from CollegiateHighGame.util.hash_map import HashMap


class Starfield(Entity):
    def __init__(self, player_views):
        super().__init__()

        self.cell_size = 300
        self.hash_map = HashMap(self.cell_size)
        self.player_views = player_views

        self.max_stars = 30

    def update(self):
        # print(self.player_views[0].coords)
        # print(self.player_views[1].coords)
        # print(self.hash_map.grid)

        # for view in self.player_views:
        #     query = self.hash_map.query_area(
        #         view.coords.topleft, view.coords.width, view.coords.height
        #     )
        #     for cell, point in query:
        #         if len(cell) == 0:
        #             # print(cell)
        #             self.fill_with_stars(point)

        pass

    def draw(self):
        for view in self.player_views:
            query = self.hash_map.query_area(
                view.coords.topleft, view.coords.width, view.coords.height
            )
            for cell, point in query:
                if len(cell) != 0:
                    for pos in cell:
                        # print(pos)
                        offset_coords = Vector2(pos) - Vector2(
                            view.coords.x, view.coords.y
                        )
                        pygame.draw.rect(
                            view.surface,
                            (255, 255, 255),
                            pygame.Rect(offset_coords[0], offset_coords[1], 2, 2),
                        )
            # pygame.draw.circle(view.surface, (255, 255, 255), pos, 1)
            # print(cell)
            # self.fill_with_stars(point)

    def fill_with_stars(self, point):
        print("Fill me")
        for i in range(randrange(self.max_stars)):
            x, y = point
            x += randrange(self.cell_size)
            y += randrange(self.cell_size)

            self.hash_map.add([x, y], (x, y))

    def prefill(self, star_count, max_x, max_y):
        print("Filling the sky with stars...")
        start = time.clock()
        for i in range(star_count):
            x = randrange(max_x)
            y = randrange(max_y)

            self.hash_map.add([x, y], (x, y))
        passed = time.clock() - start
        print(f"The sky is lit. Took {passed} seconds")
