import socket
from ..Session_Layer.Node_Struct import Node

class DataChain:
    def __init__(self, ip):
        """
        Initialize the DataChain instance.

        :param ip: The IP address of this node.
        """
        self.ip = ip  # IP address of this node
        self.next = Node.get_next_alive(self)  # Find the next alive node in the chain
        self.Chain_Port = 5003  # Port for chain communication
        self.Tail_Port = 5004  # Port for tail updates
        self.Head = self.ip  # Initially set this node as the head
        self.isHead = False  # Indicates if this node is the head of the chain
        self.prev = None  # Previous node in the chain
        self.tail = None  # Tail node in the chain

    def fetch_and_set_next(self):
        """
        Handle requests to fetch and set the next node.

        This method listens for incoming connections on `Chain_Port`. When a connection
        is received, it sends this node's IP and the head node's IP to the next node
        and updates `self.next` with the next alive node.
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((self.ip, self.Chain_Port))  # Bind to the chain port
            server_socket.listen(5)  # Listen for incoming connections
            conn, addr = server_socket.accept()  # Accept a connection
            with conn:
                data = conn.recv(1024).decode()  # Receive data from the client
                if data == "FETCH_NEXT":  # Check if the request is to fetch the next node
                    next_node = Node.get_next_alive(self)  # Get the next alive node
                    conn.sendall(f"{self.ip},{self.Head}".encode())  # Send back IP and Head
                    self.next = next_node  # Update the next node

    def get_and_set_attribute(self, ip, head_ip):
        """
        Update the previous node and head IP based on input.

        :param ip: IP address of the previous node.
        :param head_ip: IP address of the head node.
        """
        self.prev = ip  # Update the previous node
        self.Head = head_ip  # Update the head IP

    def head_listen(self):
        """
        Listen for requests to send the next node's IP to the head.

        This method is active only if `self.isHead` is True. It listens on `Chain_Port`
        for incoming requests and sends back the next node's IP.
        """
        if self.isHead:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
                server_socket.bind((self.ip, self.Chain_Port))  # Bind to the chain port
                server_socket.listen(5)  # Listen for incoming connections
                conn, addr = server_socket.accept()  # Accept a connection
                with conn:
                    data = conn.recv(1024).decode()  # Receive data from the client
                    if data == "SEND_NEXT_TO_HEAD":  # Check if the request is valid
                        conn.sendall(self.next.encode())  # Send the next node's IP

    def send_next_to_head(self):
        """
        Send the IP of the next node to the head.

        This method connects to the head node and sends a request to receive the next node's IP.
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((self.Head, self.Chain_Port))  # Connect to the head
            client_socket.sendall("SEND_NEXT_TO_HEAD".encode())  # Request next IP
            response = client_socket.recv(1024).decode()  # Receive the response
            print(f"Received next IP from head: {response}")  # Print the received IP

    def send_shard(self, target_ip, shard_data):
        """
        Send shard data to a specific IP.

        :param target_ip: IP address of the target node.
        :param shard_data: Data to be sent as a shard.
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((target_ip, self.Chain_Port))  # Connect to the target node
            client_socket.sendall(shard_data.encode())  # Send the shard data

    def update_tail(self):
        """
        Start the chain update process from the tail.

        This method sends the tail node's IP to the previous node. Each node updates
        its `tail` attribute upon receiving the message, and the process continues
        until the head node is reached.
        """
        if self.tail is None:
            print("This node is not the tail, skipping update process.")
            return

        current_node = self
        while current_node.prev:
            # Send the tail IP to the previous node
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect((current_node.prev, self.Tail_Port))
                client_socket.sendall(self.tail.encode())  # Send the tail IP
                current_node = current_node.prev  # Move to the previous node

    def listen_for_tail_update(self):
        """
        Listen for incoming tail update messages.

        This method listens on `Tail_Port` and updates the `self.tail` attribute
        when a valid message is received.
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((self.ip, self.Tail_Port))  # Bind to the tail update port
            server_socket.listen(5)  # Listen for incoming connections
            while True:
                conn, addr = server_socket.accept()  # Accept a connection
                with conn:
                    data = conn.recv(1024).decode()  # Receive the tail update message
                    self.tail = data  # Update the tail attribute
                    print(f"Tail updated to: {self.tail}")  # Log the updated tail
