import pygame


class Button:
    def __init__(self, x, y, width, height, color, text):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.text = text

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, surface):
        pass
