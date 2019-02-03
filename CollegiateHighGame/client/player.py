import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()

        self.surf = pygame.Surface((50, 50))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()

        self.x = 0
        self.y = 0

        self.network_updates = []

    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self.surf, (self.x, self.y))

    def move(self, x, y):
        self.x += x
        self.y += y

        # self.network_updates.appen

    # def get_network_updates(self):
