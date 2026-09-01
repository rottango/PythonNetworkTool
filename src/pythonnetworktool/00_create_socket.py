# wiritng a socket in python

import socket as s

class connection():
    def __init__(self):
        self.sock = s.socket(
        family=s.AF_INET, # for IPv4
        type=s.SOCK_STREAM, # for TCP
        proto=s.ETH_P_ALL, # for capturing every packet, regardless of protocol
        fileno=None) # for no auto-detect from file descriptor
        
        self.port = 50007
        
    def bind_to_address(self):
        self.sock.bind((s.INADDR_ANY,self.port))
    
    def listen_on_something(self):
        self.sock.listen(1)

    def conn_address(self):
        self.conn, self.address = self.sock.accept()
    
    def print_output(self):
        print("Connected by ", self.address)
        while True:
            data=self.conn.recv(1024)
            if not data:
                break
            self.conn.sendall(data)
