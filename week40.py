"""Simple TCP client - server application. This script must be executed with
the argument either 's' or 'c', to start a server or a client, respectively.
Only one client can be served at a time.
"""

import socket
import sys

ADDRESS = '127.0.0.1'   # server's IP address
PORT = 9999             # server's port
BUFSIZE = 1024          # size of the buffer for received data

class Server:
    """TCP server which understands just 3 commands.

    The server is supposed to run indefinitely, however it is not detached
    from its controlling terminal and can be stopped by pressing Ctrl-C.
    """

    def __init__(self, address, port):

        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.my_socket.bind((address, port))
        self.conn = None
        self.addr = None
        # dispatch table for all available commands
        self.cmd = {'say': self._say,
                    'increment': self._increment,
                    'bye': self._bye}

    def run(self):
        """Runs the server and handles messages received from the client."""
       
        print('Server started')
        # after the client disconnets the new one can be served
        while True:
            self.my_socket.listen()
            self.conn, self.addr = self.my_socket.accept()
            # context manager assures that socket will be closed when finished
            with self.conn:
                print(f'Accepted connection from {self.addr[0]} on port {self.addr[1]}')
                self.conn.sendall(b'Server is listening...')
                # handling client - server exchanges 
                while True:
                    # first element of the list is command, second, if any, is payload
                    data = self.conn.recv(BUFSIZE).decode('utf-8').split(' ', 1)
                    if not data[0]:
                        print('Client has crashed')
                        break
                    if data[0] in self.cmd:
                        # for a valid command make sure that list always has
                        # second element
                        data.append('')
                        # all command processing methods return False, except
                        # the method processing 'bye' command which returns
                        # True, that terminates connection with the client
                        if self.cmd[data[0]](data[1]):
                            break
                    else:
                        self._unknown(data[0])
            
    def _say(self, msg):
        """Sends an echo to the client."""

        self.conn.sendall(msg.encode('utf-8'))
        return False

    def _increment(self, value):
        """Sends to the client an incremented number."""

        try:
            num = int(value)
        except ValueError:
            self.conn.sendall(f'Invalid number: {value}'.encode('utf-8'))
            return False
        self.conn.sendall(str(num + 1).encode('utf-8'))        
        return False

    def _bye(self, ignore):
        """Sends final good-bye to the client."""

        self.conn.sendall(b'bye')
        print('Client has signed-off')
        return True

    def _unknown(self, arg):
        """Responds to unrecognised command."""

        self.conn.sendall(f'Unknown command: {arg}'.encode('utf-8'))

    def close(self):
        self.my_socket.close()
        

class Client:
    """Keyboard-driven TCP client.

    The client sends commands to the server and displays responses, it terminates
    upon the 'bye' command. Because the server is capable of serving only one
    client at a time, the client make sure first that it has server's attention.
    """
    
    def __init__(self, address, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(3)     # 3 seconds timeout
        self.addr = address
        self.port = port

    def run(self):
        """Runs the client and displays server's responses."""

        # context manager will close an opened socket on exit
        with self.sock as s:
            try:
                s.connect((self.addr, self.port))
            except ConnectionRefusedError:
                print('Can not connect to the server')
                sys.exit(0)
            try:
                print(f'{s.recv(BUFSIZE).decode("utf-8")}')
            except socket.timeout:
                print('Server is busy')
                sys.exit(0)
            # after receiving initial server's message the client knows that
            # connection has been established, assumes timeout not needed now
            s.settimeout(None)
            # handling client - server exchanges
            while True:
                send = input('MESSAGE TO SEND: ')
                s.sendall(send.encode('utf-8'))
                print(f'RESPONSE: {s.recv(BUFSIZE).decode("utf-8")}')
                if send == 'bye':
                    break


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Argument 's' or 'c' expected")
        sys.exit(0) 
    if sys.argv[1] == 's':
        server = Server(ADDRESS, PORT)
        try:
            server.run()
        except KeyboardInterrupt:
            server.close()
            print(' Good bye!')
            sys.exit(0)
    elif sys.argv[1] == 'c':
        client = Client(ADDRESS, PORT)
        client.run()
    else:
        print(f'Unknown argument: {sys.argv[1]}')

