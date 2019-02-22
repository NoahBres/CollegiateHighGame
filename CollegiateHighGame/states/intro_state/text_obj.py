import os
import pygame


class TextObject:
    align_center = 0
    align_left = 1
    align_right = 2

    def __init__(self, text, size, x, y, color, align=0):
        base_path = os.path.dirname(__file__)
        font_path = os.path.abspath(
            os.path.join(base_path, os.path.pardir, os.path.pardir)
        )
        font_path = os.path.join(
            font_path, "assets", "fonts", "kenvector_future_thin.ttf"
        )

        self.text = text
        self.size = size
        self.color = color
        self.font = pygame.font.Font(font_path, self.size)

        self.x = x
        self.y = y

        self.align = align

    def draw(self, surface):
        text = self.font.render(self.text, True, self.color)

        text_rect = text.get_rect()
        if self.align == TextObject.align_center:
            text_rect.centerx = self.x
            text_rect.centery = self.y
        elif self.align == TextObject.align_left:
            text_rect.x = self.x
            text_rect.y = self.y

        surface.blit(text, text_rect)

    # Really no need to be reactive
    # @property
    # def size(self):
    #     return self.__size

    # @size.setter
    # def size(self, size):
    #     self.__size = size
    #     self.font = pygame.font.SysFont(None, self.size)
