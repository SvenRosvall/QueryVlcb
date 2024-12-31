import socket
import time
from GridConnect import *

class CbusServerConnection:
    def __init__(self, host="localhost", port=5550):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((host, port))
        except:
            print("Could not connect to CBUS Server")
            exit(1)
        self.sock.settimeout(1.0)

    def askRaw(self, gcFrame):
        self.sock.send(gcFrame.encode())

        responses=[]
        gcMessage = ''
        startTime = time.time()
        while time.time() < startTime + 1.0:
            #print("Waiting for data...")
            try:
                data = self.sock.recv(128)
            except socket.timeout:
                #print("End of data")
                break
            #print("Got some data: ", data)

            for c in data.decode():
                if c == ':': # Start of new CAN frame
                    gcMessage = ''
                    continue

                if c == ';': # End of CAN frame
                    #print("Got a CAN Frame:", gcMessage)
                    responses.append(GCtoCAN(gcMessage))

                gcMessage += c

        return responses
