# Query nodes on the bus.
# Send QNN and collect PNN responses.

from sys import argv
from CbusServerConnection import *
from CbusInfo import *

def hibyte(n: int) -> int:
    return n >> 8

def lobyte(n: int) -> int:
    return n & 0xFF

if len(argv) > 1:
    nn=int(argv[1])
else:
    nn=0 # Default is SLIM nodes

cbusConnection=CbusServerConnection() 
responses = cbusConnection.askMessage(canmessage(data = [OPC_RQNPN, hibyte(nn), lobyte(nn), 0]))

paramResponses=[]
for canFrame in responses:
    if canFrame.get_op_code() == OPC_PARAN :
        #canFrame.print()
        # showCbusMessage(canFrame)
        paramResponses.append(canFrame)
#print(f"Got {len(paramResponses)} responses.")

if not paramResponses:
    print("No responses from nodes with NN =", nn)
    exit(0)

if paramResponses[0].data[3] != 0:
    print("The first response is not the number of parameters")
    exit(0)
nParams = paramResponses[0].data[4]
#print(f"Node has {nParams} parameters")

parameters={}
if len(paramResponses) == 1:
    # Need to get the params one by one.
    #print("will get each param one by one")
    for i in range(nParams):
        responses = cbusConnection.askMessage(canmessage(data = [OPC_RQNPN, hibyte(nn), lobyte(nn), i+1]))
        for canFrame in responses:
            if canFrame.get_op_code() == OPC_PARAN :
                #showCbusMessage(canFrame)
                parameters[canFrame.data[3]] = canFrame.data[4]
                break
else:
    for canFrame in paramResponses[1:]:
        parameters[canFrame.data[3]] = canFrame.data[4]

#print(f"Got {len(parameters)} parameters")        

print("Module type:", manufacturerName(parameters[PAR_MANU]),
      moduleName(parameters[PAR_MTYP]),
      f"{parameters[PAR_MAJVER]}{chr(parameters[PAR_MINVER])}{parameters[PAR_BETA]}")
print("Module flags:", flags(parameters[PAR_FLAGS]))
print("CPU:", cpuName(parameters[PAR_CPUMAN], parameters[PAR_CPUID]))