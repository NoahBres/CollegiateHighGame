from threading import Thread
import socket


class UdpServer(Thread):
    def __init__(self, address, udp_port, lock, parent):
        Thread.__init__(self)
        self.lock = lock
        self.address = address
        self.udp_port = int(udp_port)
        self.is_listening = True

        self.sock = None
        self.parent = parent

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

            # try:
            #     pass
            #     try:
            #         self.lock.acquire()
            #         pass
            #     finally:
            #         self.lock.release()
            # except Error:
            #     print("error")
        self.stop()

    def stop(self):
        self.sock.close()
