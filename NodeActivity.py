# Report error counts for each VLCB node on the bus.

from CbusServerConnection import *
from GetNodeInfo import *

def printNodeInfo(nn:int) :
    services = findServiceIndices(cbusConnection, nn)

    if SERVICE_ID_MNS in services:
        mnsSvcIdx = services[SERVICE_ID_MNS]
        acted = getDiagValue(cbusConnection, nn, mnsSvcIdx, 0x06)
    else:
        acted = -1

    if SERVICE_ID_CONSUMER in services:
        evConsIdx = services[SERVICE_ID_CONSUMER]
        evConsumed = getDiagValue(cbusConnection, nn, evConsIdx, 0x01)
    else:
        evConsumed = -1

    if SERVICE_ID_PRODUCER in services:
        evProdIdx = services[SERVICE_ID_PRODUCER]
        evProduced = getDiagValue(cbusConnection, nn, evProdIdx, 0x01)
    else:
        evProduced = -1

    if SERVICE_ID_OLD_TEACH in services:
        evTeachIdx = services[SERVICE_ID_OLD_TEACH]
        evTaught = getDiagValue(cbusConnection, nn, evTeachIdx, 0x01)
    else:
        evTaught = -1

    print(f"{nn:5} {acted:5}    {evConsumed:5}    {evProduced:5}  {evTaught:5}")

cbusConnection=CbusServerConnection() 

print("Node# Acted Consumed Produced Taught")
for node in findVlcbNodes(cbusConnection) :
    #print("Found nn:", node)
    printNodeInfo(node)