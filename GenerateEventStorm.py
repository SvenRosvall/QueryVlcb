from CbusServerConnection import *
from vlcbdefs import *

cbusConnection=CbusServerConnection()

for i in range(100):
    cbusConnection.sendMessage(CanMessage(op_code=OPC_ASON, event_node_number=999, event_number=i+1))
    