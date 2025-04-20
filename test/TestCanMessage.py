import unittest
from CanMessage import *

class TestCanMessage(unittest.TestCase):
    def test_CreateSimpleMessage(self):
        msg = CanMessage(op_code=0x17)
        self.assertEqual(0x17, msg.get_op_code())
        self.assertEqual("[580] [1] [ 17 ] ", str(msg))

    def test_CreateLongMessage(self):
        msg = CanMessage(op_code=0xFF, parameters=[2, 3, 4, 5, 6, 7, 8])
        self.assertEqual("[580] [8] [ ff 02 03 04 05 06 07 08 ] ", str(msg))

    def test_CreateMessageWithInvalidDataLength(self):
        with self.assertRaises(ValueError):
            msg = CanMessage(op_code=0xFF)

    def test_CreateMessageWithCanid(self):
        msg = CanMessage(canid=0x42, op_code=0x17)
        self.assertEqual("[5c2] [1] [ 17 ] ", str(msg))
        self.assertEqual(0x42, msg.get_canid())

    def test_CreateRtrMessage(self):
        msg = CanMessage(rtr=True)
        self.assertEqual("[580] [0] [  ] R", str(msg))

    def test_CreateExtendedMessage(self):
        msg = CanMessage(ext=True)
        self.assertEqual("[580] [0] [  ] X", str(msg))


    def test_CreateMessageWithOpCodeAndNodeNumber(self):
        msg = CanMessage(op_code=0x42, node_number=0x0123)
        self.assertEqual(0x42, msg.get_op_code())
        self.assertEqual(0x0123, msg.get_node_number())
        self.assertEqual("[580] [3] [ 42 01 23 ] ", str(msg))

    def test_CreateMessageWithOpCodeNodeNumberAndParams(self):
        msg = CanMessage(op_code=0x94, node_number=0x1234, parameters=[0x17, 0x42])
        self.assertEqual(0x94, msg.get_op_code())
        self.assertEqual(0x1234, msg.get_node_number())
        self.assertEqual(5, msg.dlc)
        self.assertEqual("[580] [5] [ 94 12 34 17 42 ] ", str(msg))
