from vlcbdefs import *
from vlcbdictionaries import *
from canmessage import canmessage

def nodeNumber(h: int, l:int):
    return (h<<8) + l

def manufacturerName(id: int):
    manu = VlcbManufacturer[id]
    if manu:
        return manu
    else:
        return "Unknown"

def moduleName(id: int):
    name = VlcbMergModuleTypes[id]
    if name:
        return name
    else:
        return "Unknown"

def flags(f: int):
    return "-"

def showCbusMessage(canFrame: canmessage):
    if canFrame.data[0] == OPC_PNN :
        print("PNN NN=", nodeNumber(canFrame.data[1], canFrame.data[2]),
              " Manufacturer=", manufacturerName(canFrame.data[3]),
              " ModuleID=", moduleName(canFrame.data[4]),
              " Flags=", flags(canFrame.data[5]),
              sep='')
    else:
        print("Unsupported OP code:", canFrame.data[0], VlcbOpCodes[canFrame.data[0]])
