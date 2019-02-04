import hashlib
import socket
from time import time


class Client:
    def __init__(self, sock, address, tcp_port, udp_port):
        self.id = Client.get_unique_id()
        self.address = address
        self.tcp_port = int(tcp_port)
        self.udp_port = int(udp_port)
        self.sock = sock

        self.props = {}

    def send_tcp(self, payload):
        if isinstance(payload, str):
            payload = str.encode(payload)

        self.sock.send(payload)

    def send_udp(self, payload):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        if isinstance(payload, str):
            payload = str.encode(payload)

        print((self.address, self.udp_port), payload)

        sock.sendto(payload, (self.address, self.udp_port))

    @staticmethod
    def get_unique_id():
        hash = hashlib.sha1()
        hash.update(str(time()).encode("utf-8"))
        return hash.hexdigest()[:10]
        # only takes last 10 to shorten the id. Hopefully wont get any collisions, otherwise, don't shorten it
