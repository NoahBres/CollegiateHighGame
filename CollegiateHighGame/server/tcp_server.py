from threading import Thread
import socket


class TcpServer(Thread):
    def __init__(self, address, tcp_port, lock, parent):
        Thread.__init__(self)

        self.lock = lock
        self.address = address
        self.tcp_port = int(tcp_port)
        self.is_listening = True

        self.lock = None
        self.parent = parent

    def run(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.address, self.tcp_port))
        self.sock.setblocking(False)
        self.sock.settimeout(5)

        self.sock.listen(1)

        while self.is_listening:
            try:
                conn, addr = self.sock.accept()
            except socket.timeout:
                continue

            data = conn.recv(1024)
            print(data)

            try:
                pass
            finally:
                self.lock.release()

            conn.close()

        self.stop()

    def stop(self):
        self.sock.close()
