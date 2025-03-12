# Query nodes on the bus.
# Send QNN and collect PNN responses.

from CbusServerConnection import *
from CbusInfo import *

def printNodeInfo(nn:int) :
    services = cbusConnection.askMessages(CanMessage(data = [OPC_RQSD, hibyte(nn), lobyte(nn), 0]))
    svcCount = -1
    canSvcIdx = -1
    canSvcVer = -1
    for svc in services :
        if svc.get_op_code() != OPC_SD : continue
        if svc.get_node_number() != nn : continue
        if svc.data[3] == 0 : svcCount = svc.data[5]
        if svc.data[4] == SERVICE_ID_CAN : 
            canSvcIdx = svc.data[3]
            canSvcVer = svc.data[5]
        
    print("Node", nn, "svc count=", svcCount, "CAN svc index=", canSvcIdx, "svc ver=", canSvcVer)
    cbusConnection.sendMessage(CanMessage(data = [OPC_RDGN, hibyte(nn), lobyte(nn), canSvcIdx, 0x11]))
    resp = cbusConnection.receiveMessage()
    #print("TX Dgn nn=", nodeNumber(resp.data[1], resp.data[2]), "ix=", resp.data[3], "code=", resp.data[4], "value=", resp.data[5], resp.data[6])
    txHW = (resp.data[5] << 8) + resp.data[6]

    cbusConnection.sendMessage(CanMessage(data = [OPC_RDGN, hibyte(nn), lobyte(nn), canSvcIdx, 0x12]))
    resp = cbusConnection.receiveMessage()
    #print("RX Dgn nn=", nodeNumber(resp.data[1], resp.data[2]), "ix=", resp.data[3], "code=", resp.data[4], "value=", resp.data[5], resp.data[6])
    rxHW = (resp.data[5] << 8) + resp.data[6]

    print("Node", nn, "TX high watermark=", txHW, "RX high watermark=", rxHW)

cbusConnection=CbusServerConnection() 

cbusConnection.sendMessage(CanMessage(data = [OPC_QNN]))
vlcbNodes = []
for canFrame in cbusConnection.receiveMessages():
    if canFrame.get_op_code() == OPC_PNN :
        #canFrame.print()
        showCbusMessage(canFrame)
        flags = canFrame.data[5]
        if flags & PF_VLCB != 0 :
            nn = nodeNumber(canFrame.data[1], canFrame.data[2])
            vlcbNodes.append(nn)

for node in vlcbNodes :
    print("Found nn:", node)
    printNodeInfo(node)