from threading import Thread
import socket


class TcpServer(Thread):
    def __init__(self, address, tcp_port, lock, listener):
        Thread.__init__(self)

        self.lock = lock
        self.address = address
        self.tcp_port = int(tcp_port)
        self.is_listening = False

        self.sock = None
        self.listener = listener

    def run(self):
        self.is_listening = True

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.address, self.tcp_port))
        # self.sock.setblocking(False)
        # self.sock.settimeout(5)

        self.sock.listen(1)

        while self.is_listening:
            try:
                try:
                    conn, addr = self.sock.accept()
                except socket.timeout:
                    continue

                data = conn.recv(1024)
                print(addr)

                try:
                    self.lock.acquire()

                    self.listener(data, conn)
                finally:
                    self.lock.release()

                conn.close()
            except socket.error as e:
                print(e)

        self.stop()

    def stop(self):
        self.sock.close()


class TcpClient(Thread):
    def __init__(self, address, tcp_port, lock, listener):
        Thread.__init__(self)
        self.lock = lock
        self.address = address
        self.tcp_port = int(tcp_port)
        self.is_listening = False

        self.sock = None
        self.listener = listener

    def run(self):
        self.is_listening = True
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.address, self.tcp_port))

        while self.is_listening:
            try:
                self.lock.acquire()

                data = self.sock.recv(1024)
                if data:
                    self.listener(data, self.sock)
            finally:
                self.lock.release()

        self.stop()

    def stop(self):
        self.sock.close()
