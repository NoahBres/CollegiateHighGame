import time

import pygame
from pygame import locals

from CollegiateHighGame.states.state import State
from .text_obj import TextObject

# from .button import Button

# Joystick button reference:
# x = 0, a = 1, b = 2, y = 3, L = 4, R = 5, select = 8, start = 9

WHITE = (255, 255, 255)


class IntroState(State):
    def __init__(self, *args, **kwargs):
        # State.__init__(self)
        super().__init__(*args, **kwargs)

        self.player1_joystick = None
        self.player2_joystick = None

        self.title = TextObject(
            "Test Title",
            60,
            self.game.center_width,
            self.game.center_height - self.game.height / 4,
            WHITE,
        )

        self.joystick_connected_text = TextObject(
            f"{self.game.joystick_count} Joystick(s) Connected",
            20,
            self.game.center_width,
            self.game.height - 40,
            WHITE,
        )

        self.press_enter_to_start = TextObject(
            "Press anything to start",
            30,
            self.game.center_width,
            self.game.center_height,
            WHITE,
        )

        self.player1_joystick_text = TextObject(
            "Player 1 Joystick (press A):",
            20,
            10,
            self.game.height - 70,
            WHITE,
            TextObject.align_left,
        )

        self.player2_joystick_text = TextObject(
            "Player 2 Joystick (press B):",
            20,
            10,
            self.game.height - 40,
            WHITE,
            TextObject.align_left,
        )

    def update(self, delta_time):
        seconds = time.time()
        # Blink text
        self.press_enter_to_start.color = (
            WHITE if (seconds * 1.5) % 2 > 1 else (0, 0, 0)
        )

        string1 = "selected" if (self.player1_joystick is not None) else ""
        string2 = "selected" if (self.player2_joystick is not None) else ""
        self.player1_joystick_text.text = f"Player 1 Joystick (press A): {string1}"
        self.player2_joystick_text.text = f"Player 2 Joystick (press B): {string2}"

    def draw(self, screen):
        screen.fill((0, 0, 0))

        self.title.draw(screen)
        self.joystick_connected_text.draw(screen)
        self.press_enter_to_start.draw(screen)
        self.player1_joystick_text.draw(screen)
        self.player2_joystick_text.draw(screen)

    def poll_events(self, events):
        for event in events:
            if event.type == locals.KEYUP:
                self.emit("start-pressed")

        for i in range(self.game.joystick_count):
            joystick = pygame.joystick.Joystick(i)
            joystick.init()

            buttons = joystick.get_numbuttons()
            for j in range(buttons):
                button = joystick.get_button(j)

                if button == 1:
                    if j == 1:
                        self.player1_joystick = i
                        if self.player2_joystick == i:
                            self.player2_joystick = None
                    if j == 2:
                        self.player2_joystick = i
                        if self.player1_joystick == i:
                            self.player1_joystick = None

                    if j == 9:
                        self.emit("start-pressed")
