# Show uptime for each VLCB node on the bus.

from CbusServerConnection import *
from CbusInfo import *

def printNodeInfo(nn:int) :
    services = cbusConnection.askMessages(CanMessage(op_code=OPC_RQSD, node_number=nn, parameters=[0]))
    svcCount = -1
    mnsSvcIdx = -1
    mnsSvcVer = -1
    for svc in services :
        if svc.get_op_code() != OPC_SD : continue
        if svc.get_node_number() != nn : continue
        if svc.data[3] == 0 : svcCount = svc.data[5]
        if svc.data[4] == SERVICE_ID_MNS : 
            mnsSvcIdx = svc.data[3]
            mnsSvcVer = svc.data[5]

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