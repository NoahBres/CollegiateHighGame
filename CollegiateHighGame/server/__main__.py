import argparse

from .server import Server

parser = argparse.ArgumentParser()

parser.add_argument("--address", dest="address", help="IP Address", default="0.0.0.0")
parser.add_argument(
    "--tcpport", dest="tcp_port", help="Listening tcp port", default="1234"
)
parser.add_argument(
    "--udpport", dest="udp_port", help="Listening udp port", default="1234"
)

args = parser.parse_args()

if __name__ == "__main__":
    server = Server(args.address, args.tcp_port, args.udp_port)
    server.start()
