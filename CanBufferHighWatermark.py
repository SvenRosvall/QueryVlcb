# Report HighWatermark for CAN buffers for each VLCB node on the bus.

from CbusServerConnection import *
from GetNodeInfo import *

def printNodeInfo(nn:int) :
    canSvcIdx = findServiceIndex(cbusConnection, nn, SERVICE_ID_CAN)
    txHW = getDiagValue(cbusConnection, nn, canSvcIdx, 0x11)
    rxHW = getDiagValue(cbusConnection, nn, canSvcIdx, 0x12)
    print(f"{nn:5}  {txHW:3} {rxHW:3}")

cbusConnection=CbusServerConnection() 

print("Node#  High Watermarks")
print("        TX  RX")
for node in findVlcbNodes(cbusConnection) :
    #print("Found nn:", node)
    printNodeInfo(node)