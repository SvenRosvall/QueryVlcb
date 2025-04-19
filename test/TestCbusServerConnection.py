import unittest
from CbusServerConnection import *
from MockNetworkConnection import *

class TestCbusServerConnection(unittest.TestCase):
    def setUp(self):
        self.connection = MockNetworkConnection()
        self.cbus = CbusServerConnection(self.connection)

    def testSendMessage(self):
        self.cbus.sendMessage(CanMessage(canid=0x42, op_code=0x17))
        sentData = self.connection.getSentData()
        decodedData = bytes(sentData).decode()
        self.assertEqual(":SB840N17;", decodedData)

    def testReceiveMessage(self):
        self.connection.setReceivedData(":SB840N17;")
        msg = self.cbus.receiveMessage()
        self.assertEqual(0x42, msg.get_canid())
