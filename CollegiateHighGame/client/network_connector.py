import threading
import socket

from CollegiateHighGame.network_handler.udp_handler import UdpHandler
from CollegiateHighGame.network_handler.tcp_handler import TcpClient

# from CollegiateHighGame.network_handler.tcp_handler import TcpHandler


class NetworkConnector:
    def __init__(self, address, tcp_port, udp_port, udp_addr):
        self.id = None

        self.address = address
        self.tcp_port = tcp_port
        self.udp_port = udp_port
        self.udp_addr = udp_addr

        self.client_udp = (address, int(udp_addr))
        self.lock = threading.Lock()

        self.udp_server = UdpHandler(address, udp_addr, self.lock, self.on_udp_message)
        self.tcp_client = TcpClient(address, tcp_port, self.lock, self.on_tcp_message)
        # self.tcp_server = TcpHandler(address, tcp_port, self.lock, self.on_tcp_message)
        self.udp_server.start()
        self.tcp_client.start()
        # self.tcp_server.start()
        self.server_udp = (address, int(udp_port))
        self.server_tcp = (address, int(tcp_port))

    def register(self):
        print("Registering")
        self.send_tcp(f"reg,{self.udp_addr}")

    def send_udp(self, package):
        if isinstance(package, str):
            package = str.encode(package)

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(package, self.server_udp)

    def send_tcp(self, package):
        if isinstance(package, str):
            package = str.encode(package)

        self.tcp_client.sock.send(package)

    def on_udp_message(self, message, sock):
        print(message)

    def on_tcp_message(self, message, sock):
        print(message)

    def close(self):
        self.udp_server.is_listening = False
        self.tcp_client.is_listening = False
