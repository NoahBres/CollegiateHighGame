import argparse
from .game import Game

parser = argparse.ArgumentParser()

parser.add_argument("--address", dest="address", help="IP Address", default="0.0.0.0")
parser.add_argument(
    "--tcpport", dest="tcp_port", help="Listening tcp port", default="1234"
)
parser.add_argument(
    "--udpport", dest="udp_port", help="Listening udp port", default="1234"
)
parser.add_argument(
    "--udpaddr", dest="udp_addr", help="UDP Address to identify by", default="1235"
)

args = parser.parse_args()

if __name__ == "__main__":
    game = Game(args.address, args.tcp_port, args.udp_port, args.udp_addr)
    game.run()
