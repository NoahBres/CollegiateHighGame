import os
import pygame


class CaptureUI:
    def __init__(self, point, sprite_name, captures):
        self.point = point
        self.rect = pygame.Rect(point, (0, 0))

        self.captures = captures

        self.padding = {"left": 10, "right": 10, "top": 5, "bottom": 5}
        self.margin_flag = 10

        base_path = os.path.dirname(__file__)
        base_path = os.path.abspath(
            os.path.join(base_path, os.path.pardir, os.path.pardir)
        )

        image_path = os.path.join(
            base_path, "assets", "entities", f"{sprite_name}.png"
        )

        self.image = pygame.image.load(image_path).convert_alpha()

        scale = 0.3
        size = self.orig_image.get_size()

        scaled_dimen = ((int(size[0] * scale)), int(size[1] * scale))
        self.image = pygame.transform.smoothscale(self.orig_image, scaled_dimen)

        self.rect = self.image.get_rect()

        self.rect.height = self.image.get_height() * 2
        self.rect.y = self.point[1] - self.rect.height

        self.surface = pygame.Surface((self.rect.width, self.rect.height))
        
        self.redraw()

    def set_captures(self, captures):
        self.captures = captures
        self.redraw()

    def redraw(self):
        self.rect.width = 0
        self.rect.width += self.margin_flag * self.count - 1
        self.rect.width += sum(self.padding['left'], self.padding['right'])
        self.rect.width += self.image.get_width() * self.count

        self.surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)

        cursor = self.padding['left']
        for i in range(self.count):
            self.surface.blit(self.image, (cursor, self.padding['top']))
            cursor += self.image.get_width() + self.margin_flag

    def draw(self, surface):
        surface.blit(self.surface, self.rect)