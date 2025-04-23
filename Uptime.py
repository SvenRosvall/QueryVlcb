# Show uptime for each VLCB node on the bus.

from CbusServerConnection import *
from CbusInfo import *

def printNodeInfo(nn:int) :
    mnsSvcIdx = findServiceIndex(cbusConnection, nn, SERVICE_ID_MNS)
    upHigh = getDiagValue(cbusConnection, nn, mnsSvcIdx, 0x02)
    upLow = getDiagValue(cbusConnection, nn, mnsSvcIdx, 0x03)

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