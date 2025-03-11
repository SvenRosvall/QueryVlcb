class MockNetworkConnection:

    def __init__(self):
        self.sentData = []
        self.dataToReceive = []

    def getSentData(self):
        return self.sentData

    def setReceivedData(self, data):
        self.dataToReceive.append(data)

    def sendData(self, data):
        self.sentData.extend(data)

    def receiveData(self):
        if not self.dataToReceive:
            return None
        nextMessage = self.dataToReceive.pop(0)
        return bytes(nextMessage, 'ascii')