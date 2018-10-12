"""Simple TCP client - server application. This script must be executed with
the argument either 's' or 'c', to start a server or a client, respectively.
Only one client can be served at a time.
"""

import socket
import sys
import pickle
import random
import string

SERVER = '127.0.0.1'    # server's IP address
PORT = 9999             # server's port
BUFSIZE = 1024          # size of the buffer for received data

class Thing:
    """Silly class for testing transmission of pickled custom object over the
    TCP link.
    """

    def __init__(self):
        self.size = random.choice(['microscopic', 'small', 'medium', 'big', 'gigantic'])
        self.shape = random.choice(['square', 'circle', 'triangle', 'ellipse', 'hexagon'])
        self.color = random.choice(['blue', 'yellow', 'green', 'red', 'black', 'white'])

    def __repr__(self):
        return f'Thing: color = {self.color}, size = {self.size}, shape = {self.shape}'


class Server:
    """TCP server which understands a few commands.

    The server is supposed to run indefinitely, however it is not detached
    from its controlling terminal and can be stopped by pressing Ctrl-C.
    """

    def __init__(self, port):

        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.my_socket.bind((socket.gethostbyname('localhost'), port))
        self.my_socket.listen()
        self.conn = None
        self.addr = None
        # dispatch table for all available commands, together with descriptions
        # of optional arguments 
        self.cmd = {'characters': (self.characters, '[string]'),
                    'echo': (self.echo, '[string]'),
                    'numbers': (self.numbers, '[integer]'),
                    'random': (self.random, None),
                    'thing': (self.thing, None),
                    'bye': (self.bye, None)}

    def run(self):
        """Runs the server and handles messages received from the client."""
       
        print('Server started')
        # after the client disconnets the new one can be served
        while True:
            self.conn, self.addr = self.my_socket.accept()
            # context manager assures that socket will be closed when finished
            with self.conn:
                print(f'Accepted connection from {self.addr[0]} on port {self.addr[1]}')
                # send to the client list of avilable commands
                funcs = [key if value[1] is None else key + ' ' + value[1]
                         for key, value in self.cmd.items()]
                msg = ('Available commands, some with optional argument:\n\t' +
                       '\n\t'.join(funcs) + '\nServer is listening...')
                self.conn.sendall(msg.encode()) 
                # handling client - server exchanges 
                while True:
                    # command and its argument, if any
                    received = self.conn.recv(BUFSIZE).decode()
                    if not received:
                        print('Client has crashed')
                        break
                    command, *data = received.split()
                    if command in self.cmd:
                        # all command processing methods return False, except
                        # the method processing 'bye' command which returns
                        # True, that terminates connection with the client
                        if self.cmd[command][0](data):
                            break
                    else:
                        self._unknown(command)
            
    def echo(self, msg):
        """Sends an echo to the client."""

        self.conn.sendall(self._pickle(' '.join(msg)))
        return False

    def numbers(self, n):
        """By default sends a list of 10 integers, the number of integers can
        be specified as an argument.
        """

        if len(n) > 0:
            try:
                num = int(n[0])
                msg = [i for i in range(num)]
            except ValueError:
                msg = f'Invalid number: {n[0]}'
        else:
            msg = [i for i in range(10)]
        self.conn.sendall(self._pickle(msg))
        return False

    def random(self, ignored):
        """Sends a random number between 0 and 1."""

        self.conn.sendall(self._pickle(random.random()))
        return False

    def characters(self, data):
        """By default sends a set of lowercase ASCII characters, if a string
        is passed to this method it returns a set of all unique characters.
        """

        if len(data) == 0:
            chars = set(string.ascii_lowercase)
        else:
            chars = set(''.join(data))
        self.conn.sendall(self._pickle(chars))
        return False

    def thing(self, ignored):
        """Sends a random Thing object."""

        self.conn.sendall(self._pickle(Thing()))
        return False

    def bye(self, ignore):
        """Sends final good-bye to the client."""

        self.conn.sendall(self._pickle('bye'))
        print('Client has signed-off')
        return True

    def _unknown(self, arg):
        """Responds to unrecognised command."""

        self.conn.sendall(self._pickle(f'Unknown command: {arg}'))

    def _pickle(self, obj):
        """Returns a pickled object or an error message when pickling was not
        possible.
        """

        try:
            bytes = pickle.dumps(obj, protocol=pickle.HIGHEST_PROTOCOL)
        except pickle.PicklingError:
            bytes = b'Internal server error - pickling'
        return bytes

    def close(self):
        """Closes server's listening socket."""

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
                print(f'{s.recv(BUFSIZE).decode()}')
            except socket.timeout:
                print('Server is busy')
                sys.exit(0)
            # after receiving initial server's message the client knows that
            # connection has been established, assumes timeout not needed now
            s.settimeout(None)
            # handling client - server exchanges
            while True:
                send = input('MESSAGE TO SEND: ')
                s.sendall(send.encode())
                received = s.recv(BUFSIZE)
                try:
                    obj = pickle.loads(received)
                except pickle.UnpicklingError:
                    obj = 'Can not unpickle the received object'
                print(f'RESPONSE: {obj}\n\t{type(obj)}')
                if send == 'bye':
                    break


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Argument 's' or 'c' expected")
        sys.exit(0) 
    if sys.argv[1] == 's':
        server = Server(PORT)
        try:
            server.run()
        except KeyboardInterrupt:
            server.close()
            print(' Good bye!')
            sys.exit(0)
    elif sys.argv[1] == 'c':
        client = Client(SERVER, PORT)
        client.run()
    else:
        print(f'Unknown argument: {sys.argv[1]}')

