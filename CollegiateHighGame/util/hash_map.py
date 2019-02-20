import itertools
from math import ceil
from collections import defaultdict

import time


class HashMap:
    def __init__(self, cell_size):
        self.cell_size = cell_size
        self.grid = defaultdict(list)

        self.last_query_list_length = 2
        self.last_area_query_points = []
        self.last_area_query_list = []

    def key(self, point):
        return (
            int(round(point[0] / self.cell_size) * self.cell_size),
            int(round(point[1] / self.cell_size) * self.cell_size),
        )

    def add(self, obj, point):
        key = self.key(point)
        self.grid[key].append(obj)

    def query_point(self, point):
        key = self.key(point)

        # print(f"Querying: {key}")

        return self.grid.get(key, [])

    def query_area(self, point, width, height):
        # start = time.clock()

        squares_to_query = []
        # These 2 loops almost make no difference. Thought it would be faster tho
        # for x in range(ceil(width / self.cell_size)):
        # for y in range(ceil(height / self.cell_size)):
        for x, y in itertools.product(
            range(ceil(width / self.cell_size) + 1),
            range(ceil(height / self.cell_size) + 1),
        ):
            query_x = point[0] + x * self.cell_size
            query_y = point[1] + y * self.cell_size

            squares_to_query.append(
                [self.query_point((query_x, query_y)), (query_x, query_y)]
            )

        # passed = time.clock() - start
        # print(f"Query took {passed * 1000} ms")

        return squares_to_query
