# Query nodes on the bus.
# Send QNN and collect PNN responses.

from sys import argv
from CbusServerConnection import *
from CbusInfo import *

nn=65535

cbusConnection=CbusServerConnection() 
responses = cbusConnection.askMessages(CanMessage(op_code=OPC_RQNPN, node_number=nn, parameters=[3]))

paramResponses=[]
for canFrame in responses:
    if canFrame.get_op_code() == OPC_PARAN :
        #canFrame.print()
        #showCbusMessage(canFrame)
        paramResponses.append(canFrame)
#print(f"Got {len(paramResponses)} responses.")

print(f"Found {len(paramResponses)} CANCAB units.")