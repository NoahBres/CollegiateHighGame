from threading import Lock

from CollegiateHighGame.network_handler.tcp_handler import TcpServer
from CollegiateHighGame.network_handler.udp_handler import UdpHandler

from .client import Client


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
                print("Yo yo")
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

        if message_split[0] == "reg":
            self.register_user(sock, message_split[1], addr)

    def on_udp_message(self, message, sock):
        print(message)

    def broadcast(self, action, message):
        print("broadcast")
        for client in self.clients.values():
            client.sock.send(f"{action},{message}".encode())

    def register_user(self, sock, udp_addr, addr):
        print("register new user")
        if udp_addr not in self.clients:
            self.clients[udp_addr] = Client(sock, addr[0], addr[1], udp_addr)

        sock.send(f"set_id,{self.clients[udp_addr].id}".encode())

        if len(self.clients) > 1:
            client_addrs = f"{'|'.join([c for c in self.clients.keys()])}"

            self.broadcast("client_list", client_addrs)
