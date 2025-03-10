import unittest
from CbusServerConnection import *
from MockNetworkConnection import *

class TestCbusServerConnection(unittest.TestCase):
    def setUp(self):
        self.connection = MockNetworkConnection()
        self.cbus = CbusServerConnection(self.connection)

    def testSendMessage(self):
        self.cbus.sendMessage(canmessage(canid=0x42, data=[0x17]))
        sentData = self.connection.getSentData()
        decodedData = bytes(sentData).decode()
        self.assertEqual(":SB840N17;", decodedData)
