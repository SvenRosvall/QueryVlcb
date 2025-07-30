# Report CAN error counts for each VLCB node on the bus.

from CbusServerConnection import *
from GetNodeInfo import *

def printNodeInfo(nn:int) :
    try:
        canSvcIdx = findServiceIndex(cbusConnection, nn, SERVICE_ID_CAN)
        txBufUse = getDiagValue(cbusConnection, nn, canSvcIdx, 0x04)
        txCount = getDiagValue(cbusConnection, nn, canSvcIdx, 0x06)
        rxBufUse = getDiagValue(cbusConnection, nn, canSvcIdx, 0x07)
        rxCount = getDiagValue(cbusConnection, nn, canSvcIdx, 0x09)
        idEnums = getDiagValue(cbusConnection, nn, canSvcIdx, 0x0D)
        idConflicts = getDiagValue(cbusConnection, nn, canSvcIdx, 0x0E)
        idChanges = getDiagValue(cbusConnection, nn, canSvcIdx, 0x0F)
        txHighWatermark = getDiagValue(cbusConnection, nn, canSvcIdx, 0x11)
        rxHighWatermark = getDiagValue(cbusConnection, nn, canSvcIdx, 0x12)

        print(f"{nn:5}  {rxCount:4}  {txCount:4}   {rxBufUse:3}    {txBufUse:3}    {rxHighWatermark:3}     {txHighWatermark:3}       {idEnums:3}     {idChanges:3}      {idConflicts:3}")
    except KeyError:
        print(f"{nn:5}  does not have a CAN service")

cbusConnection=CbusServerConnection() 

print("Node#   Msg Count  Buffers Used  Buffer Watermark CANID")
print("         RX    TX     RX     TX    RX      TX     Enums Changes Conflicts")
for node in findVlcbNodes(cbusConnection):
    # print("Found nn:", node)
    printNodeInfo(node)