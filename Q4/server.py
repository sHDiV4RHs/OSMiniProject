import select
import socket
import sys
from collections import defaultdict


SOCKET_LIST = []
maxNumOfClients = 100
group = defaultdict(list)

if len(sys.argv) < 2:
    print('Please run like this: python server.py portNumber')
    sys.exit()
port = int(sys.argv[1])
host = 'localhost'
recv_buffer = 4096

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((host, port))
server_socket.listen(maxNumOfClients)
SOCKET_LIST.append(server_socket)

print("Server started on " + str(port))

while True:
    ready_to_read, ready_to_write, in_error = select.select(SOCKET_LIST, [], [], 0)

    for sock in ready_to_read:
        if sock == server_socket:
            # New client
            newSock, addr = server_socket.accept()
            SOCKET_LIST.append(newSock)
            print ("Client {} connected".format(addr))

        else:
            # New Message
            try:
                data = sock.recv(recv_buffer)
                if data:
                    splittedData = data.split(' ')
                    if splittedData[0] == 'join':
                        gID = int(data[len('join') + 1: -1])
                        if sock not in group[gID]:
                            group[gID].append(sock)
                            print('{} joined '.format(sock.getpeername()) + str(gID))

                    elif splittedData[0] == 'leave':
                        gID = int(data[len('leave') + 1: -1])
                        if sock in group[gID]:
                            group[gID].remove(sock)
                            print('{} leaved '.format(sock.getpeername()) + str(gID))

                    else:
                        strGID = splittedData[0]
                        gID = int(strGID)

                        if sock in group[gID]:
                            for member in group[gID]:
                                if member != sock:
                                    try:
                                        member.send(data[len(strGID) + 1:])
                                    except:
                                        member.close()
                                        if member in SOCKET_LIST:
                                            SOCKET_LIST.remove(member)
                                        if member in group[gID]:
                                            group[gID].remove(member)

                else:
                    if sock in SOCKET_LIST:
                        SOCKET_LIST.remove(sock)

            except:
                continue

server_socket.close()
