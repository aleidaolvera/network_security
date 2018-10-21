import socket
import select
import sys

class Client():

    def __init__(self, host, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect( (host,int(port)) )

        while True:
            # client has typed somethin [sys.stdin]
            # server sends a message [s]
            inputs = [sys.stdin, s]

            read, trash1, trash2 = select.select(inputs, [], [])

            for sock in read:
                if sock == s:
                    # if sock is server, check for data
                    data = sock.recv(1024)
                    # write data to terminal
                    sys.stdout.write(data)
                    sys.stdout.write("\n")
                    sys.stdout.flush()

                # otherwise client is trying to send a message
                else:
                    # send server message
                    msg = sys.stdin.readline()
                    s.send(msg)
                    sys.stdout.write("")
                    sys.stdout.flush()
