# Trace any messages that show up on the connection.

from CbusServerConnection import *
from CbusInfo import *


cbusConnection=CbusServerConnection()

while True:
    msg = cbusConnection.receiveMessage()
    if msg is None:
        continue
    print(f"[{msg.canid>>7},{msg.canid&0x7F:03}] ", end="")
    showCbusMessage(msg)
