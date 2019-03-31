import os
import pygame


class PlayerHealth:
    def __init__(self, point, lives, health, color):
        self.point = point
        self.rect = pygame.Rect(point, (0, 0))

        self.lives = lives
        self.health = health

        self.padding = {"left": 10, "right": 10, "top": 5, "bottom": 5}
        self.margin = {"ship-right": 10, "x-right": 10, "number-right": 25}

        base_path = os.path.dirname(__file__)
        base_path = os.path.abspath(
            os.path.join(base_path, os.path.pardir, os.path.pardir)
        )

        mini_ship_path = os.path.join(
            base_path, "assets", "ui", f"playerLife1_{color}.png"
        )
        x_path = os.path.join(base_path, "assets", "ui", "numeralX.png")
        number_path = [
            os.path.join(base_path, "assets", "ui", f"numeral{str(i)}.png")
            for i in range(10)
        ]
        health_bar_left_path = os.path.join(
            base_path, "assets", "ui", f"barHorizontal_{color}_left.png"
        )
        health_bar_mid_path = os.path.join(
            base_path, "assets", "ui", f"barHorizontal_{color}_mid.png"
        )
        health_bar_right_path = os.path.join(
            base_path, "assets", "ui", f"barHorizontal_{color}_right.png"
        )

        self.mini_ship_img = pygame.image.load(mini_ship_path).convert_alpha()
        self.x_img = pygame.image.load(x_path).convert_alpha()
        self.number_img = [
            pygame.image.load(img).convert_alpha() for img in number_path
        ]
        self.health_bar_left_img = pygame.image.load(
            health_bar_left_path
        ).convert_alpha()
        self.health_bar_mid_img = pygame.image.load(health_bar_mid_path)
        self.health_bar_right_img = pygame.image.load(health_bar_right_path)

        self.max_height = max(
            [
                img.get_height()
                for img in [
                    self.mini_ship_img,
                    self.x_img,
                    self.health_bar_left_img,
                    self.health_bar_mid_img,
                    self.health_bar_right_img,
                ]
                + self.number_img
            ]
        )

        self.surface = pygame.Surface((self.rect.width, self.rect.height))

        self.redraw()

    def set_lives(self, lives):
        self.lives = lives
        self.redraw()

    def set_health(self, health):
        self.health = health
        self.redraw()

    def redraw(self):
        # Add up all the sprites used
        self.rect.width = 0
        self.rect.width += sum(self.margin.values())
        self.rect.width += sum([self.padding["left"], self.padding["right"]])
        self.rect.width += sum(
            [
                img.get_width()
                for img in [
                    self.mini_ship_img,
                    self.x_img,
                    self.number_img[0],
                    self.health_bar_left_img,
                    self.health_bar_right_img,
                ]
            ]
        )
        self.rect.width += round(self.health / 10) * self.health_bar_mid_img.get_width()

        self.rect.height = (
            self.max_height + self.padding["top"] + self.padding["bottom"]
        )
        self.rect.y = self.point[1] - self.rect.height
        self.surface = pygame.Surface(
            (self.rect.width, self.rect.height), pygame.SRCALPHA
        )

        # self.surface.fill((0, 255, 0))
        # self.surface.set_colorkey((0, 255, 0))

        # pygame.draw.rect(
        #     self.surface,
        #     (255, 255, 255),
        #     pygame.Rect(0, 0, self.rect.width, self.rect.height),
        #     2,
        # )

        cursor = self.padding["left"]
        self.surface.blit(
            self.mini_ship_img,
            (
                cursor,
                self.padding["top"]
                + (self.max_height - self.mini_ship_img.get_height()) / 2,
            ),
        )

        cursor += self.mini_ship_img.get_width() + self.margin["ship-right"]
        self.surface.blit(
            self.x_img,
            (
                cursor,
                self.padding["top"] + (self.max_height - self.x_img.get_height()) / 2,
            ),
        )

        cursor += self.x_img.get_width() + self.margin["x-right"]
        self.surface.blit(
            self.number_img[self.lives],
            (
                cursor,
                self.padding["top"]
                + (self.max_height - self.number_img[self.lives].get_height()) / 2,
            ),
        )

        cursor += self.x_img.get_width() + self.margin["number-right"]
        self.surface.blit(
            self.health_bar_left_img,
            (
                cursor,
                self.padding["top"]
                + (self.max_height - self.health_bar_left_img.get_height()) / 2,
            ),
        )

        cursor += self.health_bar_left_img.get_width()
        for i in range(round(self.health / 10)):
            self.surface.blit(
                self.health_bar_mid_img,
                (
                    cursor,
                    self.padding["top"]
                    + (self.max_height - self.health_bar_mid_img.get_height()) / 2,
                ),
            )
            cursor += self.health_bar_mid_img.get_width()

        self.surface.blit(
            self.health_bar_right_img,
            (
                cursor,
                self.padding["top"]
                + (self.max_height - self.health_bar_right_img.get_height()) / 2,
            ),
        )

    def draw(self, surface):
        surface.blit(self.surface, self.rect)
