import socket, select, sys

class Server():
    connected_clients = []

    def shout(self, socket, message):
        for client in self.connected_clients:
            if client != socket:
                message = message.strip('\n')
                client.send(message)

    def __init__(self, host, port):
        listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listen_socket.bind((host, int(port))) # this socket is bound to my port 9876
        listen_socket.listen(1)       # specify the "backlog" for this socket

        while True:
            # create the input list
            read_list = [listen_socket, sys.stdin] + self.connected_clients
            (ready_list,_,_) = select.select(read_list,[],[])

            for ready in ready_list:
                if ready is listen_socket:
                    conn, addr = ready.accept()
                    self.connected_clients += [conn]
                elif ready == sys.stdin:
                    msg = sys.stdin.readline()
                    self.shout(listen_socket,msg)
                    sys.stdout.write("")
                    sys.stdout.flush()
                else:
                    data = ready.recv(1024)
                    if len(data) == 0:
                        self.connected_clients.remove(ready)
                    else:
                        sys.stdout.write(data.rstrip())
                        sys.stdout.write("\n")
                        sys.stdout.flush()
                        self.shout(ready, data.rstrip())
