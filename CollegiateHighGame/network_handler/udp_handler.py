from threading import Thread
import socket


class UdpHandler(Thread):
    def __init__(self, address, udp_port, lock, listener):
        Thread.__init__(self)
        self.lock = lock
        self.address = address
        self.udp_port = int(udp_port)
        self.is_listening = True

        self.sock = None
        self.listener = listener

    def run(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.address, self.udp_port))
        self.sock.setblocking(False)
        self.sock.settimeout(5)

        while self.is_listening:
            try:
                data, addr = self.sock.recvfrom(1024)
            except socket.timeout:
                continue

            try:
                self.lock.acquire()

                self.listener((data, addr), self.sock)
            finally:
                self.lock.release()
        self.stop()

    def stop(self):
        self.sock.close()
