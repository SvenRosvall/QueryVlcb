from vlcbdefs import *
from vlcbdictionaries import *
from CanMessage import *

def findVlcbNodes(cbusConnection) -> [int]:
    cbusConnection.sendMessage(CanMessage(op_code=OPC_QNN))
    vlcbNodes = []
    for canFrame in cbusConnection.receiveMessages():
        if canFrame.get_op_code() == OPC_PNN:
            # canFrame.print()
            # showCbusMessage(canFrame)
            flags = canFrame.data[5]
            if flags & PF_VLCB != 0:
                nn = nodeNumber(canFrame.data[1], canFrame.data[2])
                vlcbNodes.append(nn)
    return vlcbNodes

def findServiceIndices(cbusConnection, nn) -> {}:
    services = cbusConnection.askMessages(CanMessage(op_code=OPC_RQSD, node_number=nn, parameters=[0]))
    result = {}
    for svc in services:
        if svc.get_op_code() != OPC_SD: continue
        if svc.get_node_number() != nn: continue
        if svc.data[3] == 0: continue
        result[svc.data[4]] = svc.data[3]
    return result

def findServiceIndex(cbusConnection, nn, svcType) -> int:
    indices = findServiceIndices(cbusConnection, nn)
    if svcType not in indices:
        raise KeyError(f"Cannot find service '{VlcbServiceTypes[svcType]}' ({svcType}) in node {nn}.")
    return indices[svcType]

def getDiagValue(cbusConnection, nn, svcIdx, diag):
    cbusConnection.sendMessage(CanMessage(op_code=OPC_RDGN, node_number=nn, parameters=[svcIdx, diag]))
    resp = cbusConnection.receiveMessage()
    while resp is not None and resp.data[0] != OPC_DGN:
        #print(f"Didn't get expected DGN response. svcIdx={svcIdx}, diag={diag}")
        #showCbusMessage(resp)
        resp = cbusConnection.receiveMessage()
    if resp is None:
        return -1
    value = (resp.data[5] << 8) + resp.data[6]
    if value != 0:
        rnn = (resp.data[1] << 8) + resp.data[2]
        print(f"Diag value={value}, nn={rnn} ({nn}), svcIdx={resp.data[3]} ({svcIdx}), diagCode={resp.data[4]} ({diag})")
    return value
