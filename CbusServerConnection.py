import time
from GridConnect import *
from NetworkConnection import *

class CbusServerConnection:
    def __init__(self):
        self.conn = NetworkConnection()

    def askMessage(self, canMessage : canmessage):
        return self.askRaw(CANtoGC(canMessage))

    def askRaw(self, gcFrame):
        self.conn.sendData(gcFrame.encode())

        gcMessage = ''
        startTime = time.time()
        while time.time() < startTime + 1.0:
            #print("Waiting for data...")
            data = self.conn.receiveData()
            if data is None:
                break
            #print("Got some data: ", data)

            for c in data.decode():
                gcMessage += c

                if c == ':': # Start of new CAN frame
                    gcMessage = ''
                    continue

                if c == ';': # End of CAN frame
                    #print("Got a CAN Frame:", gcMessage)
                    yield GCtoCAN(gcMessage)
