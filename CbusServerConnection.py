import time
from GridConnect import *
from NetworkConnection import *

class CbusServerConnection:
    def __init__(self):
        self.conn = NetworkConnection()

    def sendMessage(self, canMessage : canmessage):
        self.sendRawFrame(CANtoGC(canMessage))

    def sendRawFrame(self, gcFrame):
        self.conn.sendData(gcFrame.encode())

    def receiveMessage(self):
        return GCtoCAN(self.receiveRawFrame())

    def receiveMessages(self):
        for frame in self.receiveRawFrames():
            yield GCtoCAN(frame)

    def receiveRawFrame(self):
        gcFrame = ''
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
                gcFrame += c

                if c == ':': # Start of new CAN frame
                    gcFrame = ''
                    continue

                if c == ';': # End of CAN frame
                    #print("Got a CAN Frame:", gcMessage)
                    return gcFrame

    def receiveRawFrames(self):
        gcFrame = ''
        startTime = time.time()
        while time.time() < startTime + 1.0:
            #print("Waiting for data...")
            data = self.conn.receiveData()
            if data is None:
                break
            #print("Got some data: ", data)

            for c in data.decode():
                gcFrame += c

                if c == ':': # Start of new CAN frame
                    gcFrame = ''
                    continue

                if c == ';': # End of CAN frame
                    #print("Got a CAN Frame:", gcMessage)
                    yield gcFrame

    def askMessage(self, canMessage : canmessage):
        self.sendMessage(canMessage)
        return self.receiveMessage()

    def askMessages(self, canMessage : canmessage):
        self.sendMessage(canMessage)
        return self.receiveMessages()
