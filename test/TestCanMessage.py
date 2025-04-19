import unittest
from CanMessage import *

class TestCanMessage(unittest.TestCase):
    def test_CreateSimpleMessage(self):
        msg = CanMessage(data=[0x17])
        self.assertEqual("[580] [1] [ 17 ] ", str(msg))
        self.assertEqual(0x17, msg.get_op_code())

    def test_CreateLongMessage(self):
        msg = CanMessage(data=[0xFF, 2, 3, 4, 5, 6, 7, 8])
        self.assertEqual("[580] [8] [ ff 02 03 04 05 06 07 08 ] ", str(msg))

    def test_CreateMessageWithInvalidDataLength(self):
        with self.assertRaises(ValueError):
            msg = CanMessage(data=[0xFF])

    def test_CreateMessageWithCanid(self):
        msg = CanMessage(canid=0x42, data=[0x17])
        self.assertEqual("[5c2] [1] [ 17 ] ", str(msg))
        self.assertEqual(0x42, msg.get_canid())

    def test_CreateRtrMessage(self):
        msg = CanMessage(rtr=True)
        self.assertEqual("[580] [0] [  ] R", str(msg))

    def test_CreateExtendedMessage(self):
        msg = CanMessage(ext=True)
        self.assertEqual("[580] [0] [  ] X", str(msg))
