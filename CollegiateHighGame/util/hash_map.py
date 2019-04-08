import itertools
from math import ceil
from collections import defaultdict


class HashMap:
    def __init__(self, cell_size, caching=False):
        self.cell_size = cell_size
        self.grid = defaultdict(list)

        self.max_query_cache = 2
        self.query_area_cache = [(0, 0)] * self.max_query_cache

        self.caching = caching

    def key(self, point):
        return (
            int(round(point[0] / self.cell_size) * self.cell_size),
            int(round(point[1] / self.cell_size) * self.cell_size),
        )

    def add(self, obj, point):
        key = self.key(point)
        self.grid[key].append(obj)

    def delete(self, obj, point):
        key = self.key(point)
        cell = self.grid.get(key, [])

        try:
            cell.remove(obj)
        except Exception as e:
            print(e)
            print(cell)
            # print(self.grid)
        if not cell:
            del self.grid[key]
        # del self.grid[key]

    def update(self, obj, last_point, new_point):
        if last_point == new_point:
            return

        self.delete(obj, last_point)
        self.add(obj, new_point)

    def query_point(self, point):
        key = self.key(point)

        # print(f"Querying: {key}")

        return self.grid.get(key, [])

    def query_area(self, point, width, height, query_id=0):
        # start = time.clock()

        # TODO Fix query caching
        # key = self.key(point)
        key = point

        # This query introduces a 5x speedup when the player isn't moving
        if self.caching and self.query_area_cache[query_id][0] == (key, width, height):
            # passed = time.clock() - start
            # print(f"CQuery took {passed * 1000}ms")
            return self.query_area_cache[query_id][1]

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

        self.query_area_cache[query_id] = ((key, width, height), squares_to_query)

        # passed = time.clock() - start
        # print(f" Query took {passed * 1000} ms")

        return squares_to_query
