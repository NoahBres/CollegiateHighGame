import pygame
import os


class Player(pygame.sprite.Sprite):
    def __init__(self, sprite_name, surface):
        super().__init__()

        # -- Load image -- #
        base_path = os.path.dirname(__file__)
        image_path = os.path.abspath(os.path.join(base_path, os.path.pardir))
        image_path = os.path.join(image_path, "assets", "ships", f"{sprite_name}.png")

        self.orig_image = pygame.image.load(image_path).convert_alpha()
        # self.image.set_colorkey((0, 0, 0))
        self.rect = self.orig_image.get_rect()

        size = self.orig_image.get_size()

        self.scale = 0.5

        scaled_dimensions = ((int(size[0] * self.scale)), int(size[1] * self.scale))
        self.scaled_image = pygame.transform.smoothscale(
            self.orig_image, scaled_dimensions
        )
        self.image = self.scaled_image
        self.rect = self.image.get_rect()
        # -- Load Image -- #

        self.surface = surface

        # self.x = 20
        # self.y = 20
        self.cx = self.surface.get_rect().width / 2
        self.cy = self.surface.get_rect().height / 2
        self.rect.center = (self.cx, self.cy)

        self.angle = 0

    def draw(self):
        # self.surface.blit(
        #     self.image, (self.rect.center - self.rect.width / 2, self.cy - self.rect.height / 2)
        # )
        self.surface.blit(self.image, self.rect)

    @property
    def angle(self):
        return self.__angle

    @angle.setter
    def angle(self, angle):
        self.__angle = angle

        # orig_center = self.scaled_image.get_rect().center
        self.image = pygame.transform.rotate(self.scaled_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        # self.image.get_rect().center = orig_center
