import pygame
import os


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        basePath = os.path.dirname(__file__)
        imagePath = os.path.abspath(os.path.join(basePath, os.path.pardir))
        imagePath = os.path.join(imagePath, "assets", "ships", "playerShip1_red.png")
        # imagePath = os.path.join(basePath, "../assets/playerShip1_red.png")
        print(imagePath)
        self.image = pygame.image.load(imagePath).convert()
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()

        size = self.image.get_size()

        scale = 0.5
        scaled_dimensions = ((int(size[0] * scale)), int(size[1] * scale))
        scaled_image = pygame.transform.scale(self.image, scaled_dimensions)
        self.image = scaled_image
