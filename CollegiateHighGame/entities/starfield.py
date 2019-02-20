import os
import time
from random import randrange

import pygame
from pygame.math import Vector2

from .entity import Entity
from CollegiateHighGame.util.hash_map import HashMap


class Starfield(Entity):
    def __init__(self, player_views):
        super().__init__()

        # self.cell_size = 100
        self.cell_size = 300
        self.hash_map = HashMap(self.cell_size)
        self.player_views = player_views

        self.max_stars = 30

        self.star_length = 1
        self.load_images()

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
        for i, view in enumerate(self.player_views):
            query = self.hash_map.query_area(
                view.coords.topleft, view.coords.width, view.coords.height, i
            )
            for cell, point in query:
                if len(cell) != 0:
                    for pos, num in cell:
                        # print(pos)
                        offset_coords = Vector2(pos) - Vector2(
                            view.coords.x, view.coords.y
                        )
                        view.surface.blit(
                            self.star_img[num], (offset_coords[0], offset_coords[1])
                        )
            #             pygame.draw.rect(
            #                 view.surface,
            #                 (255, 255, 255),
            #                 pygame.Rect(offset_coords[0], offset_coords[1], 2, 2),
            #             )
            # # pygame.draw.circle(view.surface, (255, 255, 255), pos, 1)
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

            self.hash_map.add(([x, y], randrange(self.star_length)), (x, y))
        passed = time.clock() - start
        print(f"The sky is lit. Took {passed} seconds")

    def draw_star(self, point):

        pass

    def load_images(self):
        base_path = os.path.dirname(__file__)
        base_path = os.path.abspath(os.path.join(base_path, os.path.pardir))

        # Create paths
        star_path = [
            os.path.join(base_path, "assets", "stars", f"star{i + 1}.png")
            for i in range(3)
        ]

        # Load images
        self.star_img = list(
            map(lambda i: pygame.image.load(i).convert_alpha(), star_path)
        )

        # Scale images
        scale = 0.3
        # Really dirty. I should convert this to a normal for loop
        self.star_img = list(
            map(
                lambda i: pygame.transform.smoothscale(
                    i, (int(i.get_width() * scale), int(i.get_height() * scale))
                ),
                self.star_img,
            )
        )

        # Lower opacity - Doesn't work
        alpha = 0
        for star in self.star_img:
            star.set_alpha(alpha)

        print(self.star_img)
