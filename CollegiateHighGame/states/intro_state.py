import pygame
from .state import State


class IntroState(State):
    def __init__(self):
        State.__init__(self)

        # self.title = {
        #     "size": 60,
        #     "offset-y": -60,
        #     "color": (255, 255, 255),
        #     "font": pygame.font.SysFont(None, self.title["size"]),
        # }

    def update(self):
        pass

    def draw(self, screen):
        screen.fill((0, 0, 0))

        # title = self.title["font"].render("Test Title", True, self.title_color)

        # title_rect = title.get_rect()
        # title_rect.centerx = screen.get_rect().centerx
        # title_rect.centery = screen.get_rect().centery - self.title_offset_y

        # screen.blit(title, title_rect)

