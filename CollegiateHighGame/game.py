from sys import exit

import cProfile
import pstats

import pygame
from pygame import locals

# from .states.state import State
from .states.intro_state.intro_state import IntroState
from .states.game_state.game_state import GameState

TARGET_FPS = 60
PANIC_STEPS = 240
CAP_FRAMERATE = True

DEBUG_CPROFILE = True


class Game:
    def __init__(self):
        self.is_running = False

        # Just setting so it can pass into the states
        # self.width = width
        # self.height = height
        # self.center_width = width / 2
        # self.center_height = height / 2
        self.clock = pygame.time.Clock()

        self.dt = 1000 / TARGET_FPS
        self.accumulated_time = 0.0

    def run(self):
        if DEBUG_CPROFILE:
            pr = cProfile.Profile()
            pr.enable()

        pygame.init()
        pygame.joystick.init()
        pygame.mixer.init()

        # Setup screen
        # video_info = pygame.display.Info()

        # self.width = video_info.current_w - 500
        # self.height = video_info.current_h - 310
        # self.center_width = self.width / 2
        # self.center_height = self.height / 2

        # self.screen = pygame.display.set_mode(
        #     (self.width, self.height), pygame.RESIZABLE
        # )
        self.width = 1500
        self.height = 770
        self.center_width = self.width / 2
        self.center_height = self.height / 2

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(f"Collegiate Tech Club Game")

        self.joystick_count = pygame.joystick.get_count()
        self.current_state = IntroState(self)
        self.current_state.on("start-pressed", self.next_state)

        # Skip intro
        # self.next_state()

        self.is_running = True

        while self.is_running:
            self.accumulated_time += self.clock.get_time()

            num_update_steps = 0
            while self.accumulated_time >= self.dt:
                self.poll_events()
                self.update(self.dt)
                self.accumulated_time -= self.dt

                num_update_steps += 1
                if num_update_steps >= PANIC_STEPS:
                    self.panic()
                    break

            self.draw(self.screen)

            if CAP_FRAMERATE:
                self.clock.tick(TARGET_FPS)
            else:
                self.clock.tick()

        if DEBUG_CPROFILE:
            pygame.quit()
            pr.disable()
            pstats.Stats(pr).strip_dirs().sort_stats("time").print_stats()
            pr.dump_stats("profile")

        exit(0)

    def panic(self):
        self.accumulated_time = 0

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

        self.current_state.poll_events(events)

    def draw(self, screen):
        self.current_state.draw(screen)

        fps_font = pygame.font.Font(None, 25)
        fps = fps_font.render(
            f"{str(int(self.clock.get_fps()))} fps", True, (255, 255, 255)
        )
        screen.blit(fps, (10, 10))

        pygame.display.flip()
        # pygame.display.update()
        # pygame.display.update(pygame.Rect(100, 100, 500, 500))

    def update(self, delta_time):
        self.current_state.update(delta_time)

    def next_state(self):
        if isinstance(self.current_state, IntroState):
            self.player1_joystick = self.current_state.player1_joystick
            self.player2_joystick = self.current_state.player2_joystick
            self.current_state = GameState(self)
