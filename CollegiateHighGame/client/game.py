from sys import exit
import pygame
from pygame import locals

from .network_connector import NetworkConnector
from .player import Player
from .network_player import NetworkPlayer

(width, height) = (800, 600)
background = (0, 0, 0)

clock = pygame.time.Clock()
ticks_per_second = 60


class Game:
    def __init__(self, address, tcp_port, udp_port, udp_address):
        self.connector = NetworkConnector(
            address, tcp_port, udp_port, udp_address, self
        )

        self.tcp_port = tcp_port
        self.udp_port = udp_port
        self.udp_address = udp_address

        self.player = Player()
        self.clients = {}

        self.running = False

    def run(self):
        self.connector.register()

        while self.connector.id is None:
            pass

        pygame.init()

        screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(f"Collegiate Tech Club Game - {self.connector.id}")

        self.running = True

        try:
            while self.running:
                clock.tick(ticks_per_second)

                self.poll_events()
                self.update()
                self.draw(screen)

            self.connector.close()
            pygame.quit()
            exit(0)
        except SystemExit:
            self.connector.close()
            pygame.quit()
            exit(0)  # Redudant but ¯\_(ツ)_/¯

    def poll_events(self):
        events = pygame.event.get()
        # keys = pygame.key.get_pressed()

        # Check for quit
        for event in events:
            if event.type == locals.QUIT:
                self.running = False
                return
            if event.type == locals.KEYDOWN:
                if event.key == locals.K_ESCAPE:
                    self.running = False
                    return

    def update(self):
        self.player.update()

    def draw(self, screen):
        screen.fill(background)

        self.player.draw(screen)

        for client in self.clients.values():
            client.draw(screen)

        pygame.display.flip()

    def register_clients(self, client_list):
        client_props = [x.split(";") for x in client_list]
        new_clients = list(filter(lambda x: x[0] != self.connector.id, client_props))

        for item in new_clients:
            new_player = NetworkPlayer(item[0])
            new_player.x = item[1]
            new_player.y = item[2]
            self.clients[item[0]] = new_player
