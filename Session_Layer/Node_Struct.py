import Protocols
import threading
import time

class Node:
    def __init__(self):
        # Initialize the node with various attributes
        self.prev = None  # Previous node in the chain (could be None if no previous node exists)
        self.next = None  # Next node in the chain (could be None if no next node exists)
        self.neighbour = []  # List to store neighbors' IP addresses
        self.Head = None  # Head node in the chain (could be None if no head node exists)
        self.Tail = None  # Tail node in the chain (could be None if no tail node exists)
        self.shards = {}  # A dictionary holding shard IDs and their corresponding shard data
        self.shard_table = {}  # A dictionary mapping shard IDs to the IP addresses of their holders
        self.Session_Port = 5000  # Port used for session communication
        self.Data_Port = 5001  # Port used for data communication
        
        # Flags to manage the status of various threads
        self.session_pong_thread_running = False  # To check if the session pong thread is running
        self.data_pong_thread_running = False  # To check if the data pong thread is running
        self.ping_thread_running = False  # To check if the ping thread is running
        
        self.failed_neighbors = []  # List to store neighbors that failed the ping check

        # Lock for thread synchronization to avoid race conditions
        self.lock = threading.Lock()

        # Start all necessary threads for maintaining node connectivity and health
        self.start_session_ping_thread()
        self.start_session_pong_thread()
        self.start_data_pong_thread()

    def start_session_ping_thread(self):
        """Starts the session ping thread to periodically ping neighbors and other connected nodes."""
        if not self.ping_thread_running:
            # Set the ping_thread_running flag to True to indicate the thread is starting
            self.ping_thread_running = True
            # Create a new thread for the session ping process
            self.SessionPingThread = threading.Thread(target=self.session_ping)
            self.SessionPingThread.daemon = True  # Daemon thread: it will exit when the program exits
            self.SessionPingThread.start()  # Start the session ping thread

    def start_session_pong_thread(self):
        """Starts the session pong thread to listen for pings and respond with pongs."""
        if not self.session_pong_thread_running:
            # Set the session_pong_thread_running flag to True to indicate the thread is starting
            self.session_pong_thread_running = True
            # Create a new thread for the session pong process
            self.SessionPongThread = threading.Thread(target=self.session_pong)
            self.SessionPongThread.daemon = True  # Daemon thread: it will exit when the program exits
            self.SessionPongThread.start()  # Start the session pong thread

    def start_data_pong_thread(self):
        """Starts the data pong thread if not already running."""
        if not self.data_pong_thread_running:
            # Set the data_pong_thread_running flag to True to indicate the thread is starting
            self.data_pong_thread_running = True
            # Create a new thread for the data pong process
            self.DataPongThread = threading.Thread(target=self.data_pong)
            self.DataPongThread.daemon = True  # Daemon thread: it will exit when the program exits
            self.DataPongThread.start()  # Start the data pong thread

    def session_ping(self):
        """Periodically ping each neighbor, prev, next, head, and tail every 1 second to check for their status."""
        while self.ping_thread_running:
            with self.lock:  # Synchronize access to self.neighbour and self.failed_neighbors
                # Ping each neighbor in the neighbor list and dynamically update the failed_neighbors list
                for ip in self.neighbour[:]:  # Iterate over a copy to avoid modifying the list while iterating
                    if Protocols.Ping(ip, self.Data_Port):  # Ping the neighbor's IP and check if successful
                        print(f"Successfully pinged neighbor {ip}")
                        if ip in self.failed_neighbors:  # If the neighbor had failed before, remove it from failed list
                            self.failed_neighbors.remove(ip)
                            print(f"Removed {ip} from failed_neighbors list")
                    else:  # If ping fails, add the neighbor to the failed_neighbors list
                        print(f"Failed to ping neighbor {ip}")
                        if ip not in self.failed_neighbors:
                            self.failed_neighbors.append(ip)
                            print(f"Added {ip} to failed_neighbors list")

                # Retry failed neighbors dynamically within the same loop
                for ip in self.failed_neighbors[:]:  # Iterate over the failed_neighbors list
                    retry_count = 3  # Number of retry attempts for failed neighbors
                    failed = False
                    for attempt in range(retry_count):
                        # Try pinging the failed neighbor up to 'retry_count' times
                        if not Protocols.Ping(ip, self.Data_Port):
                            failed = True
                            print(f"Failed to ping {ip} on attempt {attempt + 1}")
                        else:
                            failed = False
                            break  # Stop retrying if the ping is successful

                    if failed:  # If still failed after retries, remove from neighbor list
                        with self.lock:
                            if ip in self.neighbour:
                                self.neighbour.remove(ip)
                                print(f"Removed {ip} from neighbour list")
                    print(f"{ip} is still in failed_neighbors list after {retry_count} attempts")

                # Check prev, next, head, tail nodes (no removal from neighbor list for these)
                check_nodes = [self.prev, self.next, self.Head, self.Tail]
                for node in check_nodes:
                    if node is not None:  # Only ping nodes that are not None
                        if Protocols.Ping(node, self.Data_Port):  # Ping the node and check for success
                            print(f"Successfully pinged node {node}")
                        else:
                            print(f"Failed to ping node {node}")

            time.sleep(1)  # Sleep for 1 second to avoid overwhelming the system with constant pings

    def data_pong(self):
        """Pong function that runs forever if prev is None. Otherwise, stops and restarts the thread."""
        while self.data_pong_thread_running:
            if self.prev is None:
                try:
                    Protocols.Pong(self, self.Data_Port)  # Respond to pings with pong message
                except Exception as e:
                    print(f"Error in Pong: {e}")
            else:
                # If prev is set (i.e., no longer the head node), stop the thread and restart it
                self.data_pong_thread_running = False
                self.start_data_pong_thread()  # Restart the data pong thread if needed
                break  # Exit the loop after restarting the thread

    def get_next_alive(self):
        """
        Finds and returns the next alive node from the neighbor list.
        Updates `self.next` with the first alive node found.
        """
        with self.lock:  # Ensure thread-safe access to the neighbor list
            for n in self.neighbour:  # Check each neighbor in the list
                if Protocols.Ping(n, self.Data_Port):  # Ping the neighbor and check if it is alive
                    self.next = n  # Update the next node if this one is alive
                    print(f"{n} is now the next node")
                    return n
        return None  # Return None if no alive neighbors are found

    def add_neighbour(self, ip_address):
        """
        Adds a new neighbor by their IP address to the neighbor list.
        
        :param ip_address: IP address of the new neighbor to add
        """
        with self.lock:  # Synchronize access to the neighbor list
            if ip_address not in self.neighbour:
                self.neighbour.append(ip_address)  # Add the new neighbor if not already present
                print(f"Added neighbour with IP: {ip_address}")
            else:
                print(f"Neighbour with IP: {ip_address} already exists.")  # Print message if the neighbor already exists
