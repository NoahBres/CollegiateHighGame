from random import randrange
import pygame

from .entity import Entity
from CollegiateHighGame.util.hash_map import HashMap


class Starfield(Entity):
    def __init__(self, player_views):
        super().__init__()

        self.cell_size = 300
        self.hash_map = HashMap(self.cell_size)
        self.player_views = player_views

        self.max_stars = 12

    def update(self):
        # print(self.player_views[0].coords)
        # print(self.player_views[1].coords)
        # print(self.hash_map.grid)

        for view in self.player_views:
            query = self.hash_map.query_area(
                view.coords.topleft, view.coords.width, view.coords.height
            )
            for cell, point in query:
                if len(cell) == 0:
                    # print(cell)
                    self.fill_with_stars(point)

    def draw(self):
        calls = 0
        for view in self.player_views:
            query = self.hash_map.query_area(
                view.coords.topleft, view.coords.width, view.coords.height
            )
            # print(len(query))
            for cell, point in query:
                if len(cell) != 0:
                    for pos in cell:
                        calls += 1
                        # print(pos)
            # pygame.draw.rect(view.surface, (255, 255, 255), pygame.Rect(pos[0], pos[1], 2, 2))
            # pygame.draw.circle(view.surface, (255, 255, 255), pos, 1)
            # print(cell)
            # self.fill_with_stars(point)
        print(calls)

    def fill_with_stars(self, point):
        for i in range(randrange(self.max_stars)):
            x, y = point
            x += randrange(self.cell_size)
            y += randrange(self.cell_size)

            self.hash_map.add([x, y], (x, y))
