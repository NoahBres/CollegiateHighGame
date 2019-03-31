import os
import pygame


class ShotCount:
    def __init__(self, point, count):
        self.point = point
        self.rect = pygame.Rect(point, (0, 0))

        self.count = count

        self.padding = {"left": 10, "right": 10, "top": 5, "bottom": 5}
        self.margin_dot = 7

        base_path = os.path.dirname(__file__)
        base_path = os.path.abspath(
            os.path.join(base_path, os.path.pardir, os.path.pardir)
        )

        dot_path = os.path.join(base_path, "assets", "ui", "dotYellow.png")

        self.dot_image = pygame.image.load(dot_path).convert_alpha()
        scale = 0.5
        size = self.dot_image.get_size()
        scaled_dimen = ((int(size[0] * scale)), int(size[1] * scale))
        self.dot_image = pygame.transform.smoothscale(self.dot_image, scaled_dimen)

        self.rect.height = self.dot_image.get_height() * 2
        self.rect.y = self.point[1] - self.rect.height

        self.surface = pygame.Surface((self.rect.width, self.rect.height))

        self.redraw()

    def set_count(self, count):
        self.count = count
        self.redraw()

    def redraw(self):
        self.rect.width = 0
        self.rect.width += self.margin_dot * self.count - 1
        self.rect.width += sum([self.padding["left"], self.padding["right"]])
        self.rect.width += self.dot_image.get_width() * self.count

        self.surface = pygame.Surface(
            (self.rect.width, self.rect.height), pygame.SRCALPHA
        )

        cursor = self.padding["left"]
        for i in range(self.count):
            self.surface.blit(self.dot_image, (cursor, self.padding["top"]))
            cursor += self.dot_image.get_width() + self.margin_dot

    def draw(self, surface):
        surface.blit(self.surface, self.rect)
