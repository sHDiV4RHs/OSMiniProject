import select
import socket
import sys


if len(sys.argv) < 4:
    print ('Please run like this: python client.py serverIP serverPort clientName')
    sys.exit()

host = sys.argv[1]
port = int(sys.argv[2])
clientName = sys.argv[3]

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(2)

try:
    s.connect((host, port))
except:
    print ('Connection Failed!')
    sys.exit()

print('Connected successfully. You are {}.'.format(clientName))

while True:
    socket_list = [sys.stdin, s]

    read_sockets, write_sockets, error_sockets = select.select(socket_list, [], [])

    for sock in read_sockets:
        if sock == s:
            # From server
            data = sock.recv(4096)
            if not data:
                s.close()
                print ('\nYou are Disconnected!')
                sys.exit()
            else:
                sys.stdout.flush()
                sys.stdout.write(data)

        else:
            # From myself
            msg = sys.stdin.readline()
            splittedMessage = msg.split(' ')
            if splittedMessage[0] == 'quit\n':
                s.close()
                print('Quit successfully.')
                sys.exit()

            elif splittedMessage[0] == 'send':
                gID = splittedMessage[1]
                s.send(gID + " " +
                       "{}: ".format(clientName) +
                       msg[len('send') + 1 + len(gID) + 1:])
            else:
                try:
                    s.send(msg)
                except:
                    s.close()
                    print ('\nYou are Disconnected!')
                    sys.exit()
