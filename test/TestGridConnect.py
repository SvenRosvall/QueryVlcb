import unittest
from GridConnect import *

class TestGridConnect(unittest.TestCase):
    def test_CANtoGC(self):
        msg = canmessage(canid=0x42, data=[0x17])
        gc = CANtoGC(msg)
        self.assertEqual(gc, ":SB840N17;")

    def test_GCtoCAN(self):
        gc = ":SB840N17;"
        msg = GCtoCAN(gc)
        self.assertEqual(msg.get_canid(), 0x42)
        self.assertEqual(msg.dlc, 1)
        self.assertEqual(list(msg.data), [0x17])

if __name__ == '__main__':
    unittest.main()
