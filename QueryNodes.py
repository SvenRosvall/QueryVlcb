# Query nodes on the bus.
# Send QNN and collect PNN responses.

from CbusServerConnection import *
from CbusInfo import *

cbusConnection=CbusServerConnection() 
responses = cbusConnection.askRaw(":S0000N0D;")

for canFrame in responses:
    if canFrame.get_op_code() == OPC_PNN :
        #canFrame.print()
        showCbusMessage(canFrame)
