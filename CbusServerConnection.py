import time
from GridConnect import *
from NetworkConnection import *

class CbusServerConnection:
    def __init__(self, connection = None):
        if connection is None:
            connection = NetworkConnection()
        self.conn = connection

        self.gcFrame = ""
        self.data = []

    def sendMessage(self, canMessage : canmessage):
        self.sendRawFrame(CANtoGC(canMessage))

    def sendRawFrame(self, gcFrame):
        self.conn.sendData(gcFrame.encode())

    def receiveMessage(self):
        return GCtoCAN(self.receiveRawFrame())

    def receiveMessages(self):
        for frame in self.receiveRawFrames():
            #print("Received frame:", frame)
            yield GCtoCAN(frame)

    def receiveRawFrame(self):
        startTime = time.time()
        while time.time() < startTime + 1.0:
            if not self.data:
                #print("Waiting for data...")
                rcv = self.conn.receiveData()
                if rcv is None:
                    break
                #print("Received some data: ", rcv)
                self.data = list(rcv.decode())
            #print("Got some data: ", self.data)

            c = self.data.pop(0)
            self.gcFrame += c

            if c == ':': # Start of new CAN frame
                self.gcFrame = ''
                continue

            if c == ';': # End of CAN frame
                #print("Got a CAN Frame:", self.gcFrame)
                return self.gcFrame

    def receiveRawFrames(self):
        startTime = time.time()
        while time.time() < startTime + 1.0:
            res = self.receiveRawFrame()
            if res is None:
                return
            yield res

    def askMessage(self, canMessage : canmessage):
        self.sendMessage(canMessage)
        return self.receiveMessage()

    def askMessages(self, canMessage : canmessage):
        self.sendMessage(canMessage)
        return self.receiveMessages()
