class MockNetworkConnection:

    def __init__(self):
        self.sentData = []

    def getSentData(self):
        return self.sentData

    def sendData(self, data):
        self.sentData.extend(data)