import uuid
from pygame import Vector2


class Entity:
    def __init__(self):
        self.hash = hash(uuid.uuid4())
        self.world_pos = Vector2(0, 0)

    def __hash__(self):
        return self.hash

    def __eq__(self, other):
        return other.hash == self.hash

    def __ne__(self, other):
        return not (self == other)

    def update(self):
        pass

    def draw(self, surface):
        pass
