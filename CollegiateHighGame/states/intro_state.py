import time

import pygame
from .state import State


class IntroState(State):
    def __init__(self, *args, **kwargs):
        # State.__init__(self)
        super().__init__(*args, **kwargs)

        # self.title = {
        #     "size": 60,
        #     "offset-y": -60,
        #     "color": (255, 255, 255),
        #     "font": pygame.font.SysFont(None, self.title["size"]),
        # }

        self.title = TextObject(
            "Test Title",
            60,
            self.game.center_width,
            self.game.center_height - self.game.height / 4,
            (255, 255, 255),
        )

        self.joystick_connected_text = TextObject(
            f"{self.game.joystick_count} Joysticks Connected",
            20,
            self.game.center_width,
            self.game.height - 40,
            (255, 255, 255),
        )

        self.press_enter_to_start = TextObject(
            "Press anything to start",
            30,
            self.game.center_width,
            self.game.center_height,
            (255, 255, 255),
        )

    def update(self):
        seconds = time.time()
        # Blink text
        self.press_enter_to_start.color = (
            (255, 255, 255) if (seconds * 1.5) % 2 > 1 else (0, 0, 0)
        )

    def draw(self, screen):
        screen.fill((0, 0, 0))

        self.title.draw(screen)
        self.joystick_connected_text.draw(screen)
        self.press_enter_to_start.draw(screen)


class TextObject:
    def __init__(self, text, size, centerx, centery, color):
        self.text = text
        self.size = size
        self.color = color
        self.font = pygame.font.SysFont(None, self.size)
        self.centerx = centerx
        self.centery = centery

    def draw(self, surface):
        text = self.font.render(self.text, True, self.color)

        text_rect = text.get_rect()
        text_rect.centerx = self.centerx
        text_rect.centery = self.centery

        surface.blit(text, text_rect)

    # Really no need to be reactive
    # @property
    # def size(self):
    #     return self.__size

    # @size.setter
    # def size(self, size):
    #     self.__size = size
    #     self.font = pygame.font.SysFont(None, self.size)


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
