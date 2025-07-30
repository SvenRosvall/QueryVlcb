import unittest
from GetNodeInfo import *
from CbusServerConnection import *
from MockNetworkConnection import *

# TODO:
# * findServiceIndices()
# * findServiceIndex()
# * getDiagValue()

class TestCbusInfo_connected(unittest.TestCase):
    def setUp(self):
        self.connection = MockNetworkConnection()
        self.cbus = CbusServerConnection(self.connection)

    def test_findVlcbNodes(self):
        resp1 = CanMessage(op_code=OPC_PNN, node_number=4711,
                           parameters=[MANU_MERG, MTYP_CANPAN, PF_SD | PF_COMBI | PF_NORMAL])
        resp2 = CanMessage(op_code=OPC_PNN, node_number=4712,
                           parameters=[MANU_MERG, MTYP_CANMIO, PF_SD | PF_COMBI | PF_NORMAL])
        # Non-VLCB nodes shall be ignored.
        resp3 = CanMessage(op_code=OPC_PNN, node_number=4713,
                           parameters=[MANU_MERG, MTYP_CANMIO, PF_COMBI | PF_NORMAL])
        self.connection.setReceivedData(CANtoGC(resp1))
        self.connection.setReceivedData(CANtoGC(resp2))
        self.connection.setReceivedData(CANtoGC(resp3))

        result = findVlcbNodes(self.cbus)

        self.assertEqual(2, len(result))
        self.assertEqual(4711, result[0])
        self.assertEqual(4712, result[1])

    def test_findServiceIndices(self):
        resp0 = CanMessage(op_code=OPC_SD, node_number=4711,
                           parameters=[0, 0, 2])
        resp1 = CanMessage(op_code=OPC_SD, node_number=4711,
                           parameters=[2, SERVICE_ID_MNS, 1])
        resp2 = CanMessage(op_code=OPC_SD, node_number=4711,
                           parameters=[3, SERVICE_ID_CAN, 1])
        self.connection.setReceivedData(CANtoGC(resp0))
        self.connection.setReceivedData(CANtoGC(resp1))
        self.connection.setReceivedData(CANtoGC(resp2))

        result = findServiceIndices(self.cbus, 4711)

        self.assertEqual(2, len(result))
        self.assertEqual(2, result[SERVICE_ID_MNS])
        self.assertEqual(3, result[SERVICE_ID_CAN])

    def test_findServiceIndex(self):
        resp0 = CanMessage(op_code=OPC_SD, node_number=4711,
                           parameters=[0, 0, 2])
        resp1 = CanMessage(op_code=OPC_SD, node_number=4711,
                           parameters=[2, SERVICE_ID_MNS, 1])
        resp2 = CanMessage(op_code=OPC_SD, node_number=4711,
                           parameters=[3, SERVICE_ID_CAN, 1])
        self.connection.setReceivedData(CANtoGC(resp0))
        self.connection.setReceivedData(CANtoGC(resp1))
        self.connection.setReceivedData(CANtoGC(resp2))

        result = findServiceIndex(self.cbus, 4711, SERVICE_ID_MNS)

        self.assertEqual(2, result)

    def test_findServiceIndex_missing(self):
        resp0 = CanMessage(op_code=OPC_SD, node_number=4711,
                           parameters=[0, 0, 2])
        resp1 = CanMessage(op_code=OPC_SD, node_number=4711,
                           parameters=[2, SERVICE_ID_MNS, 1])
        resp2 = CanMessage(op_code=OPC_SD, node_number=4711,
                           parameters=[3, SERVICE_ID_CAN, 1])
        self.connection.setReceivedData(CANtoGC(resp0))
        self.connection.setReceivedData(CANtoGC(resp1))
        self.connection.setReceivedData(CANtoGC(resp2))

        with self.assertRaises(KeyError):
            findServiceIndex(self.cbus, 4711, SERVICE_ID_EVENTACK)
