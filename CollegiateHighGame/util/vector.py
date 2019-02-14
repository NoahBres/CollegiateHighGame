from pygame.math import Vector2


class Vector(Vector2):
    def limit(self, max):
        if self.length() <= max:
            return

        self = self.normalize() * max
