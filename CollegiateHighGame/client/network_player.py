import pygame


class NetworkPlayer(pygame.sprite.Sprite):
    def __init__(self, id):
        super(NetworkPlayer, self).__init__()
        self.id = id

        self.surf = pygame.Surface((50, 50))
        self.surf.fill((255, 100, 100))
        self.rect = self.surf.get_rect()

        self.x = 0
        self.y = 0

    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self.surf, (int(self.x), int(self.y)))
