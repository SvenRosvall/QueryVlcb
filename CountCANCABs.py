# Query nodes on the bus.
# Send QNN and collect PNN responses.

from sys import argv
from CbusServerConnection import *
from CbusInfo import *

def hibyte(n: int) -> int:
    return n >> 8

def lobyte(n: int) -> int:
    return n & 0xFF

nn=65535

cbusConnection=CbusServerConnection() 
responses = cbusConnection.askMessage(canmessage(data = [OPC_RQNPN, hibyte(nn), lobyte(nn), 3]))

paramResponses=[]
for canFrame in responses:
    if canFrame.get_op_code() == OPC_PARAN :
        #canFrame.print()
        #showCbusMessage(canFrame)
        paramResponses.append(canFrame)
#print(f"Got {len(paramResponses)} responses.")

print(f"Found {len(paramResponses)} CANCAB units.")