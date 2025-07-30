# Report CAN error counts for each VLCB node on the bus.

from CbusServerConnection import *
from GetNodeInfo import *

def printNodeInfo(nn:int) :
    canSvcIdx = findServiceIndex(cbusConnection, nn, SERVICE_ID_CAN)
    rxErrCnt = getDiagValue(cbusConnection, nn, canSvcIdx, 0x01)
    txErrCnt = getDiagValue(cbusConnection, nn, canSvcIdx, 0x02)
    errStat = getDiagValue(cbusConnection, nn, canSvcIdx, 0x03)
    txBufOver = getDiagValue(cbusConnection, nn, canSvcIdx, 0x05)
    rxBufOver = getDiagValue(cbusConnection, nn, canSvcIdx, 0x08)
    rxErrFrms = getDiagValue(cbusConnection, nn, canSvcIdx, 0x0A)
    txErrFrms = getDiagValue(cbusConnection, nn, canSvcIdx, 0x0B)
    arbLost = getDiagValue(cbusConnection, nn, canSvcIdx, 0x0C)
    idFail = getDiagValue(cbusConnection, nn, canSvcIdx, 0x10)
    print(f"{nn:5}     {errStat:02X}   {rxErrCnt:3}   {txErrCnt:3}    {rxErrFrms:3}    {txErrFrms:3}     {rxBufOver:3}   {txBufOver:3}        {arbLost:3}        {idFail:3}")

cbusConnection=CbusServerConnection() 

print("Node#   Err  Error Count  Error Frames  Buffer Overrun  Arbitration  CANID")
print("       State    RX    TX     RX     TX      RX    TX       Lost      enum fail")
for node in findVlcbNodes(cbusConnection):
    # print("Found nn:", node)
    printNodeInfo(node)