import socket

class NetworkConnection:
    def __init__(self, host="localhost", port=5550):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((host, port))
        except:
            print("Could not connect to CBUS Server")
            exit(1)
        self.sock.settimeout(1.0)
        
    def sendData(self, data):
        self.sock.send(data)
        
    def receiveData(self):
        try:
            return self.sock.recv(128)
        except socket.timeout:
            return None
