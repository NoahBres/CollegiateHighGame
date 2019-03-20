import pygame


class MiniMap:
    def __init__(self, x, y, width, height, view):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.view = view

        self.background = (30, 30, 30)

        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.surface.fill(self.background)

    def update(self):
        pass

    # Could use optimizing. E.g:
    # Rather than filling the whole screen, just draw over past square coordinates
    # Ride of blending
    def draw(self, surface):
        self.surface.fill(self.background)
        pygame.draw.rect(
            self.surface, (255, 255, 255), pygame.Rect(0, 0, self.width, self.height), 1
        )

        player_square_coords = (
            self.view.player.world_pos[0] / self.view.game.width * self.width,
            self.view.player.world_pos[1] / self.view.game.height * self.height,
        )
        player_square_width = 3

        pygame.draw.rect(
            self.surface,
            (255, 0, 0),
            pygame.Rect(
                player_square_coords[0] - int(player_square_width / 2),
                player_square_coords[1] - int(player_square_width / 2),
                player_square_width,
                player_square_width,
            ),
        )

        # Why doesn't alpha work
        # self.surface.set_alpha(128)
        # surface.blit(self.surface, (self.x, self.y))
        surface.blit(
            self.surface,
            (self.x, self.y),
            pygame.Rect(0, 0, self.width, self.height),
            pygame.BLEND_RGBA_ADD,
        )
