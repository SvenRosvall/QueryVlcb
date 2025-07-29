import unittest
from CbusInfo import *


# Tests functions in CbusInfo

# TODO:
# * showCbusMessage() for each known op-code and some unknown.
# * findVlcbNodes()
# * findServiceIndices()
# * findServiceIndex()
# * getDiagValue()


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

    # TODO: Can't test this as showCbusMessage() prints rather than returning a string.
    # def test_showCbusMessage_PNN(self):
    #     self.assertEqual("PNN NN=4711 Manufacturer=MERG ModuleId=CANPAN FLAGS=CONSUMER PRODUCER NORMAL SD",
    #                      showCbusMessage(CanMessage(op_code=OPC_PNN,  node_number=4711,
    #                                                 parameters=[MANU_MERG, MTYP_CANPAN, 71])))
