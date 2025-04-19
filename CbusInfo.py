from vlcbdefs import *
from vlcbdictionaries import *
from CanMessage import *

def manufacturerName(id: int):
    manu = VlcbManufacturer[id]
    if manu:
        return manu
    else:
        return "Unknown"

def moduleName(id: int):
    if id in VlcbMergModuleTypes:
        return VlcbMergModuleTypes[id]
    else:
        return f"Unknown({id})"

def flags(f: int):
    return ' '.join([VlcbParamFlags[bitvalue]
                     for bitvalue in [1<<bit for bit in range(8)]
                     if (f & bitvalue) != 0])

def cpuName(manId: int, cpuId: int):
    if manId == CPUM_MICROCHIP:
        if cpuId in VlcbMicrochipProcessors:
            return VlcbMicrochipProcessors[cpuId]
        else:
            return f"Unknown Microchip processor(cpuId)"
    else:
        return f"Unknown CPU Manufacturer({manId})"
    

def showCbusMessage(canFrame: CanMessage):
    if canFrame.data[0] == OPC_PNN :
        print("PNN NN=", nodeNumber(canFrame.data[1], canFrame.data[2]),
              " Manufacturer=", manufacturerName(canFrame.data[3]),
              " ModuleID=", moduleName(canFrame.data[4]),
              " Flags=", flags(canFrame.data[5]),
              sep='')
    elif canFrame.data[0] == OPC_PARAN :
        print("PARAN NN=", nodeNumber(canFrame.data[1], canFrame.data[2]),
              " Parameter no: ", canFrame.data[3],
              " Parameter value=", canFrame.data[4],
              sep='')
    elif canFrame.data[0] == OPC_GRSP :
        print("GRSP NN=", nodeNumber(canFrame.data[1], canFrame.data[2]),
              "Request Op=", VlcbOpCodes[canFrame.data[3]],
              "Service=", VlcbServiceTypes[canFrame.data[4]],
              "Result=", VlcbGrspCodes[canFrame.data[5]],
              sep='')
    else:
        print("Unsupported OP code:", canFrame.data[0], VlcbOpCodes[canFrame.data[0]])
