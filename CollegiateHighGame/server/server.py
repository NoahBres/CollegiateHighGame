from threading import Lock

from CollegiateHighGame.network_handler.tcp_handler import TcpServer
from CollegiateHighGame.network_handler.udp_handler import UdpHandler


class Server:
    def __init__(self, address, tcp_port, udp_port):
        self.address = address
        self.tcp_port = tcp_port
        self.udp_port = udp_port

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

    def on_tcp_message(self, message, sock):
        print(message)
        message = message.decode()

        message_split = message.split(",")
        print(message_split)

        if message_split[0] == "reg":
            print("register new user")
            sock.send(b"test")

    def on_udp_message(self, message, sock):
        print(message)
