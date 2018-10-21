import socket
import select
import sys
from crypto import Crypto


class Client():
    global crypt

    def __init__(self, host, port, conf_key, auth_key):
        crypt = Crypto()

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
                    decrypt_data = crypt.decrypt(data, conf_key, auth_key)
                    print(decrypt_data)

                # otherwise client is trying to send a message
                else:
                    # send server message
                    msg = sys.stdin.readline()
                    msg = crypt.encrypt(msg, conf_key, auth_key)
                    s.send(msg)
