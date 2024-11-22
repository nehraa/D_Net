import socket
import time
from .Node_Struct import Node
'''
Ping(IP, Port) ping a node and expect a pong back to make sure the node is Alive 
(Later on we can specifiy port so each port supports specific activites and also how to handle packets)
Parameter : IP, Port
Return : True/False
'''
def Ping(IP, Port):
  sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Opening a UDP socket
  sock.settimeout(2)  # Set timeout to 2 seconds for waiting for PONG
  try:
    sock.sendto((63).to_bytes(1, 'big'), (IP, Port))  # 63 is the ASCII for ? (PING)
    print(f"Ping sent to {IP}")  # For testing purposes onlY
    # Wait for PONG (PONG = 1)
    try:
      data, addr = sock.recvfrom(1024)  # Listens for connection
      if data == (1).to_bytes(1, 'big'):  # PONG is represented by 1
          print(f"{IP} replied")  # For testing purposes only
          return True  # If you receive the PONG
    except socket.timeout:
        print(f"Timeout: No response from {IP} within 2 seconds.")
        return False  # If no PONG is received within the timeout
  finally:
    sock.close()  # Ensure the socket is closed no matter what


'''
Pong(self) #pong back the node to tell yes the node is Alive 
(Maybe also return some traffic and resource information to see if we have storge to keep shards)
Parameter : self
Return : None
'''
def Pong(self, port):
  sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Opening a UDP socket
  sock.bind((self.ip, port))  # Binds a socket to a port
  #try:
  while True:
    data, addr = sock.recvfrom(1024)  # Listens for connection
    if data == (63).to_bytes(1, 'big'):
      print(f"Received Ping from {addr}")  # For testing purposes only
      sock.sendto((1).to_bytes(1, 'big'), addr)  # Rather than sending PING(4 bytes) send just one
  #finally:
    #sock.close()  # Ensure the socket is closed when done