import unittest
from CbusInfo import *

# Tests functions in CbusInfo

# TODO:
# * showCbusMessage() for each known op-code and some unknown.


class TestCbusInfo(unittest.TestCase):
    def test_manufacturerName(self):
        self.assertEqual("MERG", manufacturerName(MANU_MERG))  # add assertion here

    def test_manufacturerName_unknown(self):
        self.assertEqual("Unknown(1)", manufacturerName(1))  # add assertion here

    def test_moduleName(self):
        self.assertEqual("CANPAN", moduleName(MTYP_CANPAN))

    def test_moduleName_unknown(self):
        self.assertEqual("Unknown(241)", moduleName(241))

    def test_flags(self):
        self.assertEqual("CONSUMER PRODUCER NORMAL BOOT COE LRN SD", flags(0x7F))

    def test_flags_none(self):
        self.assertEqual("", flags(0))

    def test_cpuName(self):
        self.assertEqual("P18F27Q83", cpuName(CPUM_MICROCHIP, P18F27Q83))

    def test_cpuName_unknownManu(self):
        self.assertEqual("Unknown CPU Manufacturer(0)", cpuName(0, P18F27Q83))

    def test_cpuName_unknownCpu(self):
        self.assertEqual("Unknown Microchip processor(0)", cpuName(CPUM_MICROCHIP, 0))

    def test_showCbusMessage_PNN(self):
        self.assertEqual("PNN NN=4711 Manufacturer=MERG ModuleID=CANPAN Flags=CONSUMER PRODUCER NORMAL SD",
            describeCbusMessage(CanMessage(op_code=OPC_PNN, node_number=4711,
                parameters=[MANU_MERG, MTYP_CANPAN, 71])))

    def test_showCbusMessage_PARAN(self):
        self.assertEqual("PARAN NN=4711 Parameter no: 7 Parameter value=12",
            describeCbusMessage(CanMessage(op_code=OPC_PARAN, node_number=4711,
                parameters=[7, 12])))

    def test_showCbusMessage_GRSP(self):
        self.assertEqual("GRSP NN=4711 Request Op=REVAL Service=ID_MNS Result=INVALID_MODE",
            describeCbusMessage(CanMessage(op_code=OPC_GRSP, node_number=4711,
                parameters=[OPC_REVAL, SERVICE_ID_MNS, GRSP_INVALID_MODE])))

    def test_showCbusMessage_CMDERR(self):
        self.assertEqual("CMDERR NN=4711 Result=INV_CMD",
            describeCbusMessage(CanMessage(op_code=OPC_CMDERR, node_number=4711,
                parameters=[CMDERR_INV_CMD])))

    def test_showCbusMessage_REVAL(self):
        self.assertEqual("REVAL NN=4711 Event index=7 Event variable index=3",
            describeCbusMessage(CanMessage(op_code=OPC_REVAL, node_number=4711,
                parameters=[7, 3])))

    def test_showCbusMessage_NEVAL(self):
        self.assertEqual("NEVAL NN=4711 Event index=7 EV index=3 Value=42",
            describeCbusMessage(CanMessage(op_code=OPC_NEVAL, node_number=4711,
                parameters=[7, 3, 42])))

    def test_showCbusMessage_ENRSP(self):
        self.assertEqual("ENRSP NN=4711 Event NN=5321 EN=1234 index=7",
            describeCbusMessage(CanMessage(op_code=OPC_ENRSP, node_number=4711,
                event_node_number=5321, event_number=1234, parameters=[7])))

    def test_showCbusMessage_REQEV(self):
        self.assertEqual("REQEV NN=4711 EN=1234 Event index=7",
            describeCbusMessage(CanMessage(op_code=OPC_REQEV, node_number=4711,
                event_number=1234, parameters=[7])))

    def test_showCbusMessage_EVANS(self):
        self.assertEqual("EVANS NN=4711 EN=1234 Event index=7 Value=42",
            describeCbusMessage(CanMessage(op_code=OPC_EVANS, node_number=4711,
                event_number=1234, parameters=[7, 42])))

    def test_showCbusMessage_HEARTB(self):
        self.assertEqual("HEARTB NN=4711 Seq=42 Status=17 StatusBits=3",
            describeCbusMessage(CanMessage(op_code=OPC_HEARTB, node_number=4711,
                parameters=[42, 17, 3])))

