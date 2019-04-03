import pygame


class SpeedUI:
    def __init__(self, point, dimen, percent):
        self.point = point
        self.dimen = dimen
        self.percent = percent

        self.rect = pygame.Rect(point, (dimen[0] * percent, dimen[1]))

        self.color = (255, 255, 255)

        self.redraw()

    def set_percent(self, percent):
        self.percent = percent
        self.rect.width = self.dimen[0] * self.percent

    def redraw(self):
        pass

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
