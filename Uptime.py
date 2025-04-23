# Show uptime for each VLCB node on the bus.

from CbusServerConnection import *
from CbusInfo import *

def printNodeInfo(nn:int) :
    mnsSvcIdx = findServiceIndex(cbusConnection, nn, SERVICE_ID_MNS)

    #print("Node", nn, "svc count=", svcCount, "MNS svc index=", mnsSvcIdx, "svc ver=", mnsSvcVer)
    cbusConnection.sendMessage(CanMessage(op_code=OPC_RDGN, node_number=nn, parameters=[mnsSvcIdx, 0x02]))
    resp = cbusConnection.receiveMessage()
    #print("High: nn=", nodeNumber(resp.data[1], resp.data[2]), "ix=", resp.data[3], "code=", resp.data[4], "value=", resp.data[5], resp.data[6])
    upHigh = (resp.data[5] << 8) + resp.data[6]

    cbusConnection.sendMessage(CanMessage(op_code=OPC_RDGN, node_number=nn, parameters=[mnsSvcIdx, 0x03]))
    resp = cbusConnection.receiveMessage()
    #print("Low:  nn=", nodeNumber(resp.data[1], resp.data[2]), "ix=", resp.data[3], "code=", resp.data[4], "value=", resp.data[5], resp.data[6])
    upLow = (resp.data[5] << 8) + resp.data[6]

    uptime = (upHigh << 16) + upLow
    upHour = int(uptime / 60 / 60)
    upMin = int(uptime / 60) % 60
    upSec = uptime % 60

    print(f"{nn:5} {uptime:6}  {upHour:2}:{upMin:02}:{upSec:02}")

cbusConnection=CbusServerConnection()

vlcbNodes = findVlcbNodes(cbusConnection)

print("Node#  Uptime")
for node in vlcbNodes :
    #print("Found nn:", node)
    printNodeInfo(node)