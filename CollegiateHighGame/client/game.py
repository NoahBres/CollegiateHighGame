from sys import exit
import pygame
from pygame import locals

from .network_connector import NetworkConnector
from .player import Player

(width, height) = (800, 600)
background = (0, 0, 0)

clock = pygame.time.Clock()
ticks_per_second = 60


class Game:
    def __init__(self, address, tcp_port, udp_port, udp_address):
        self.connector = NetworkConnector(
            address, tcp_port, udp_port, udp_address, self
        )
        self.running = False

        self.tcp_port = tcp_port
        self.udp_port = udp_port
        self.udp_address = udp_address

        self.clients = {}

    def run(self):
        self.connector.register()

        while self.connector.id is None:
            pass

        pygame.init()

        screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(f"Collegiate Tech Club Game - {self.connector.id}")

        self.player = Player()

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

        pygame.display.flip()

    def register_clients(self, client_list):
        print(client_list)

        new_items = set(client_list) - self.clients.keys()

        for item in new_items:
            if item != self.connector.id:
                print(f"fellow client: {item}")
