# Client

from threading import Thread
from queue import Queue
import socket
import sys


class Client:
    """ Connects to a running server at given ip address, using given username as alias

    Queues:
    log - holds the notifications about the inner workings of the client. check it for errors on networking end.
    incoming - holds the incoming messages
    outgoing - holds the outgoing messages

    """
    def __init__(self):
        """Sets up necessary instance variables
        """
        self.socket = None
        self.running = False
        self.username = ""

        self.out_thread = None
        self.in_thread = None

        self.log = Queue()
        self.incoming = Queue()
        self.outgoing = Queue()

    def connect(self, address, username):
        """ Searches for a connection at the address provided
        :param address:
        :param username:
        :return:
        """
        self.running = True
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.username = username

        # search for connection
        self.log.put("Connecting to server at ip %s:%s" % address)
        try:
            self.socket.connect(address)
        except ConnectionRefusedError as cre:
            self.log.put("[E] Could not connect to ip %s:%s" % address)
            return
        except socket.gaierror as gaie:
            self.log.put("[E] Could not gather address information")
            return
        except:
            self.log.put("[E] %s" % sys.exc_info()[0])
        # if it gets to this point, no critical errors have been found
        self.log.put("Connection established")

        # initialize the threads
        self.out_thread = Thread(target=self.send_messages)
        self.in_thread = Thread(target=self.get_messages)

        # try to start them
        try:
            self.send.start()
            self.get.start()
        except:
            self.log.put("[E] %s" % sys.exc_info()[0])

    def disconnect(self):
        """ Destroys any existing connections
        :return:
        """
        if not self.socket is None:
            try:
                #TODO: message scheme
                self.socket.sendall(bytearray(str.encode(" END MESSAGE GOES HERE ")))
            except:
                self.log.put("No oonnection was established...")
            self.running = False
            self.log.put("Disconnecting...")
            if self.out_thread.is_alive():
                self.out_thread.join()
            if self.in_thread.is_alive():
                self.in_thread.join()
            try:
                self.socket.shutdown(socket.SHUT_RDWR)
                self.socket.close()
                self.socket = None
            except:
                self.log.put("[E] %s" % sys.exc_info()[0])

        pass

    def get_messages(self):
        """ Receives messages from the server which are stored in the in_thread to be processed by main thread
        :return:
        """
        try:
            while self.running:
                data = self.socket.recv()
                if not data == b"":
                    self.in_thread.put(data.decode("utf-8"))
        except:
            self.log.put("[E] %s" % sys.exc_info()[0])
        pass

    def send_messages(self):
        """ Sends messages to the server
        :return:
        """
        while self.running:
            info = ""
            if not self.out_thread.empty():
                info = self.out_thread.get()
            try:
                if not info == "":
                    self.socket.sendall(bytearray(str.encode(info)))
                    self.log.put(info)
            except:
                self.log.put("[E] %s" % sys.exc_info()[0])
        pass
