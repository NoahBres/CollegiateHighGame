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

        self.title = TextObject()
        self.title.text = "Test Title"
        self.title.size = 60
        self.title.centerx = self.game.center_width
        self.title.centery = self.game.center_height - self.game.height / 4

        self.joystick_connected_text = TextObject()
        self.joystick_connected_text.text = (
            f"{self.game.joystick_count} Joysticks Connected"
        )
        self.joystick_connected_text.size = 20
        self.joystick_connected_text.centerx = self.game.center_width
        self.joystick_connected_text.centery = self.game.center_height

    def update(self):
        pass

    def draw(self, screen):
        screen.fill((0, 0, 0))

        self.title.draw(screen)
        self.joystick_connected_text.draw(screen)


class TextObject:
    def __init__(self):
        self.text = ""
        self.size = 14
        self.color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, self.size)
        self.centerx = 0
        self.centery = 0

    def draw(self, surface):
        text = self.font.render(self.text, True, self.color)

        text_rect = text.get_rect()
        text_rect.centerx = self.centerx
        text_rect.centery = self.centery

        surface.blit(text, text_rect)

    @property
    def size(self):
        return self.__size

    @size.setter
    def size(self, size):
        self.__size = size
        self.font = pygame.font.SysFont(None, self.size)


class Button:
    def __init__(self):
        pass
