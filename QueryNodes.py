# Query nodes on the bus.
# Send QNN and collect PNN responses.

from canmessage import canmessage
from CbusServerConnection import *
from CbusInfo import *

cbusConnection=CbusServerConnection() 
responses = cbusConnection.askRaw(":S0000N0D;")

for canFrame in responses:
    canFrame.print()
    showCbusMessage(canFrame)
