import argparse
from client import Client
from server import Server

parser = argparse.ArgumentParser()
parser.add_argument('-c', action='append')
parser.add_argument('-s', action='store_true')
parser.add_argument('-p', action='append')
args = parser.parse_args()
if args.s:
    if args.p:
        port = int(args.p[0])
        server = Server("", port)
if args.c:
    port = int(args.p[0])
    host = args.c[0]
    client = Client(host, port)
