# Report error counts for each VLCB node on the bus.

from CbusServerConnection import *
from CbusInfo import *

def printNodeInfo(nn:int) :
    mnsSvcIdx = findServiceIndex(cbusConnection, nn, SERVICE_ID_MNS)
    status = getDiagValue(cbusConnection, nn, mnsSvcIdx, 0x01)
    memFault = getDiagValue(cbusConnection, nn, mnsSvcIdx, 0x04)
    print(f"{nn:5}  {status:3} {memFault:3x}")

cbusConnection=CbusServerConnection() 

print("Node# Status Memory Fault")
for node in findVlcbNodes(cbusConnection) :
    #print("Found nn:", node)
    printNodeInfo(node)