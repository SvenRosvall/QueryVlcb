# Query nodes on the bus.
# Send QNN and collect PNN responses.

from CbusServerConnection import *
from CbusInfo import *

cbusConnection=CbusServerConnection() 
responses = cbusConnection.askMessages(CanMessage(op_code = OPC_QNN))

for canFrame in responses:
    if canFrame.get_op_code() == OPC_PNN :
        #canFrame.print()
        showCbusMessage(canFrame)
