from math import floor


class HashMap:
    def __init__(self, cell_size):
        self.cell_size = cell_size
        self.grid = {}

    def key(self, point):
        return (
            int(round(point[0] / self.cell_size) * self.cell_size),
            int(round(point[1] / self.cell_size) * self.cell_size),
        )

    def add(self, obj, point):
        key = self.key(point)
        if self.grid.get(key) is None:
            self.grid[key] = []
        self.grid[key].append(obj)
        # self.grid.get(key, []).append(obj)

    def query_point(self, point):
        key = self.key(point)
        return self.grid.get(key, [])

    def query_area(self, point, width, height):
        squares_to_query = []
        for x in range(floor(width / self.cell_size)):
            for y in range(floor(height / self.cell_size)):
                query_x = point[0] + x * self.cell_size
                query_y = point[1] + y * self.cell_size
                squares_to_query.append(
                    [self.query_point((query_x, query_y)), (query_x, query_y)]
                )

        return squares_to_query
