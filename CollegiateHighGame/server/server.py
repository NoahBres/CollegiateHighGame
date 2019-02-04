from threading import Lock
import json

from CollegiateHighGame.network_handler.tcp_handler import TcpServer
from CollegiateHighGame.network_handler.udp_handler import UdpHandler

from .client import Client


# TODO Switch the abbreivated network commands to enums that both client and server share
class Server:
    def __init__(self, address, tcp_port, udp_port):
        self.address = address
        self.tcp_port = tcp_port
        self.udp_port = udp_port

        self.clients = {}

    def start(self):
        lock = Lock()

        udp_server = UdpHandler(self.address, self.udp_port, lock, self.on_udp_message)
        tcp_server = TcpServer(self.address, self.tcp_port, lock, self.on_tcp_message)

        udp_server.start()
        tcp_server.start()

        is_running = True

        print("Game Server")
        print("------------------------")
        print("list - lists connected users")
        # print("")
        print("------------------------")

        while is_running:
            cmd = input("> ")
            if cmd == "list":
                print(self.clients)
            elif cmd == "quit":
                print("Shutting down server...")
                udp_server.is_listening = False
                tcp_server.is_listening = False
                is_running = False

        udp_server.join()
        tcp_server.join()

    def on_tcp_message(self, message, sock, addr):
        print(message)
        message = message.decode()

        message_split = message.split(",")
        print(message_split)

        action = message_split[0]
        payload = message_split[1]

        if action == "reg":
            self.register_user(sock, payload, addr)

    def on_udp_message(self, message, sock):
        print(message)
        message = message[0].decode()

        message_split = message.split(";")
        print(message_split)

        origin = message_split[0]
        payload = json.loads(message_split[1])

        for item in payload:
            action = item[0]
            sub_payload = item[1]
            if action == "m":
                # props_to_update = {"x": sub_payload[0], "y": sub_payload[1]}
                # self.update_player(origin, props_to_update)

                player = next(
                    (x for x in self.clients.values() if x.id == origin), None
                )
                player.x = sub_payload[0]
                player.y = sub_payload[1]

                self.broadcast_udp_except(
                    "pm", json.dumps([origin, (player.x, player.y)]), origin
                )

    def broadcast_tcp(self, action, message):
        print("broadcast_tcp")
        for client in self.clients.values():
            client.send_tcp(f"{action};{message}")

    def broadcast_tcp_except(self, action, message, exceptions):
        print(f"broadcast_tcp except: {exceptions}")
        for client in self.clients.values():
            if client.id not in exceptions:
                client.send_tcp(f"{action};{message}")

    def broadcast_udp(self, action, message):
        print("broadcast_udp")
        for client in self.clients.values():
            client.send_udp(f"{action};{message}")

    def broadcast_udp_except(self, action, message, exceptions):
        print(f"broadcast_udp except: {exceptions}")
        for client in self.clients.values():
            if client.id not in exceptions:
                client.send_udp(f"{action};{message}")

    def register_user(self, sock, udp_addr, addr):
        print("register new user")
        new_client = None
        if udp_addr not in self.clients:
            new_client = Client(sock, addr[0], addr[1], udp_addr)
            self.clients[udp_addr] = new_client
        else:
            new_client = self.clients[udp_addr]

        new_client_x = 10 if len(self.clients) == 1 else 740
        new_client_y = 275 if len(self.clients) == 1 else 275

        new_client.props["x"] = new_client_x
        new_client.props["y"] = new_client_y
        print()

        payload = json.dumps((self.clients[udp_addr].id, new_client_x, new_client_y))
        sock.send(f"set_id;{payload}".encode())

        if len(self.clients) > 1:
            client_addrs = [
                (c.id, c.props["x"], c.props["y"]) for c in self.clients.values()
            ]
            client_addrs = json.dumps(client_addrs)

            self.broadcast_tcp("client_list", client_addrs)

    def update_player(self, id, props):
        player = next((x for x in self.clients.values() if x.id == id), None)

        if player is None:
            return

        for item in props:
            player.props[item] = props[item]

        print(player.props)
