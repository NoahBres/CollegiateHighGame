from sys import exit
import pygame

from pygame import locals

# from .states.state import State
from .states.intro_state import IntroState

(width, height) = (800, 600)

clock = pygame.time.Clock()
ticks_per_second = 60


class Game:
    def __init__(self):
        self.is_running = False
        self.current_state = IntroState()

    def run(self):
        pygame.init()

        screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(f"Collegiate Tech Club Game")

        self.is_running = True

        while self.is_running:
            self.poll_events()
            self.update()
            self.draw(screen)

            clock.tick(ticks_per_second)

        pygame.quit()
        exit(0)

    def poll_events(self):
        events = pygame.event.get()

        for event in events:
            if event.type == locals.QUIT:
                self.is_running = False
                return
            if event.type == locals.KEYDOWN:
                if event.key == locals.K_ESCAPE:
                    self.is_running = False
                    return

        self.current_state.poll_events()

    def draw(self, screen):
        # screen.fill((255, 0, 0))
        self.current_state.draw(screen)

        pygame.display.flip()

    def update(self):
        self.current_state.update()
