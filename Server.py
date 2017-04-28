# Server

from queue import Queue
from restartablethread import RestartableThread
import socket
import sys

# final variables

max_connections = 4
address = sys.argv[0]


# end final variables


class Server:
    """ Hosts a server on given ip address through port 7777

    server_address - address that the server is hosting on port 7777
    running - whether or not the server is in the on or off state

    Queues:
    log - holds the notifications about the inner workings of the server. check it for errors on networking end.
    connection_queue - holds the connection requests waiting to be resolved
    input_queue - holds the incoming messages
    output_queue - holds the outgoing messages

    """

    def __init__(self):
        """Sets up necessary instance variables
        """
        self.connection_dict = dict()
        self.thread_dict = dict()
        self.user_dict = dict()
        self.packet_size = 1024
        self.max_connections = max_connections
        self.running = False
        self.server_address = ""
        self.socket = None
        # init threads
        self.connection_queue = Queue()
        self.input_queue = Queue()
        self.output_queue = Queue()
        self.log = Queue()
        self.client_thread = RestartableThread(target=self.accept_connections)
        self.reply_thread = RestartableThread(target=self.reply)

    def start(self, server_address):
        """ Seeks connection requests on server address given in param.
        :param server_address:
        :return:
        """

        # set state to running
        self.running = True

        # initialize server socket
        self.server_address = server_address
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # bind address
        self.log.put("Starting on %s:%s" % self.server_address)
        self.sock.bind(self.server_address)

        # socket -> server mode
        self.socket.listen(1)

        # begin listening for connection requests
        try:
            self.log.put("Starting Threads...")
            self.client_thread.start()
            self.reply_thread.start()
        except EOFError:
            self.client_thread.join()
            self.reply_thread.join()

    def destroy(self):
        """ Terminates all existing connections and stops accepting new ones.
        :return:
        """
        if self.running:
            self.running = False
        if self.client_thread.is_alive():
            self.force_destroy()
            self.client_thread.join()
            self.client_thread = self.client_thread.clone()

    def force_destroy(self):
        """ Creates a fake client so that the server can break out of its accept() state and be terminated
        :return:
        """
        fake_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            fake_client.connect(self.server_address)
            fake_client.shutdown(socket.SHUT_RDWR)
            fake_client.close()
        except:
            self.log.put("[E] %s" % sys.exc_info()[0])

    def accept_connections(self):
        current_connections = 0
        while current_connections < self.max_connections:
            # break if the server should be off
            if not self.running:
                break
            self.log.put("Waiting for a connection...")
            client = self.socket.accept()
            # just in case it was hung up on accept(), check again
            if not self.running:
                break
            # if it passes accept(), somebody has connected
            self.log.put("Client connected from:", client[1])
            self.connection_queue.put(client)
        else:
            client.socket.accept()
            self.log.put("Kicking client from:", client[1], "(Reached Max Capacity)")
            client[0].sendall(bytearray(str.encode("Server full.")))

    def reply(self):
        """ Sends messages back to clients
        :return:
        """
        while self.running:
            info = b""
            try:
                # initialize new threads for new connections
                if not self.connection_queue.empty():
                    # get connection off of queue
                    item = self.connection_queue.get()
                    # add to the connection dictionary
                    # (conn, address) bound by address
                    self.connection_dict[item[1]] = item
                    # create a new thread for it
                    connection_thread = RestartableThread(target=self.listen, args=(item,))
                    connection_thread.start()
                    # add connection's thread to thread dictionary
                    self.thread_dict[item[1]] = connection_thread
                else:
                    # no new connections
                    pass
            except:
                self.log.put("[E] Failed to add more clients to the thread dictionary")
                print("Error: %s" % sys.exc_info()[0])
            try:
                if not self.output_queue.empty():
                    # if there is something to send out
                    info = self.output_queue.get()
                    self.log.put("[D] Sending out: %s" % info)
                if not info == b"":
                    # possible commands
                    if __name__ == '__main__':
                        if __name__ == '__main__':
                            for iter_connection in self.connection_dict.values():
                                connection, client_address = iter_connection
                                # TODO: message scheme
                                try:
                                    connection.sendall(bytearray(str.encode(info)))
                                except:
                                    # a client must have left...
                                    self.log.put("[E] Unexpected client problems")
                                    pass
            finally:
                pass

    def listen(self, client):
        """ Manages a connection's input forwards it into the input queue
        :param client:
        :return:
        """
        connection, client_address = client
        while self.running:
            info = ""
            try:
                data = connection.recv()
                # data is in a bytearray so we cast it back to a string
                info = data.decode("utf-8")
            except:
                pass
            if len(info) == 0:
                # end the thread, because it must have disconnected
                # TODO: message scheme; currently clients can't disconnect
                self.input_queue.put()
                break
            if not info == "":
                # TODO: message scheme
                info = self.user_dict[client_address] + ": " + data.decode("utf-8")
                self.input_queue(info)
