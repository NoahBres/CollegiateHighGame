import uuid
from pygame import Vector2


class Entity:
    def __init__(self):
        self.hash = hash(uuid.uuid4())
        self.world_pos = Vector2(0, 0)

        self.orig_rect = None
        self.rect = None

        self.depose = False

        # 0 is topmost
        # Drawing importance goes down
        # E.g 0 will be drawn above 1, 1 drawn above 2, etc.
        # Player (topmost drawn) should probably be 0
        self.draw_level = 0

    def __hash__(self):
        return self.hash

    def __eq__(self, other):
        return other.hash == self.hash

    def __ne__(self, other):
        return not (self == other)

    def update(self, delta_time):
        pass

    def draw(self, surface):
        pass

    def collide(self, entity):
        pass
