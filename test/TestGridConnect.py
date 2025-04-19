import unittest
from GridConnect import *

class TestGridConnect(unittest.TestCase):
    def test_CANtoGC(self):
        msg = CanMessage(canid=0x42, op_code=0x17)
        gc = CANtoGC(msg)
        self.assertEqual(":SB840N17;", gc)

    def test_GCtoCAN(self):
        gc = ":SB840N17;"
        msg = GCtoCAN(gc)
        self.assertEqual(0x42, msg.get_canid())
        self.assertEqual(1, msg.dlc)
        self.assertEqual([0x17], list(msg.data))

if __name__ == '__main__':
    unittest.main()
