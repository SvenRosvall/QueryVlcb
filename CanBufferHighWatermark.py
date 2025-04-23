# Report HighWatermark for CAN buffers for each VLCB node on the bus.

from CbusServerConnection import *
from CbusInfo import *

def printNodeInfo(nn:int) :
    canSvcIdx = findServiceIndex(cbusConnection, nn, SERVICE_ID_CAN)

    #print("Node", nn, "svc count=", svcCount, "CAN svc index=", canSvcIdx, "svc ver=", canSvcVer)
    cbusConnection.sendMessage(CanMessage(op_code=OPC_RDGN, node_number=nn, parameters=[canSvcIdx, 0x11]))
    resp = cbusConnection.receiveMessage()
    #print("TX Dgn nn=", nodeNumber(resp.data[1], resp.data[2]), "ix=", resp.data[3], "code=", resp.data[4], "value=", resp.data[5], resp.data[6])
    txHW = (resp.data[5] << 8) + resp.data[6]

    cbusConnection.sendMessage(CanMessage(op_code=OPC_RDGN, node_number=nn, parameters=[canSvcIdx, 0x12]))
    resp = cbusConnection.receiveMessage()
    #print("RX Dgn nn=", nodeNumber(resp.data[1], resp.data[2]), "ix=", resp.data[3], "code=", resp.data[4], "value=", resp.data[5], resp.data[6])
    rxHW = (resp.data[5] << 8) + resp.data[6]

    print(f"{nn:5}  {txHW:3} {rxHW:3}")

cbusConnection=CbusServerConnection() 

print("Node#  High Watermarks")
print("        TX  RX")
for node in findVlcbNodes(cbusConnection) :
    #print("Found nn:", node)
    printNodeInfo(node)