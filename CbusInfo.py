from vlcbdefs import *
from vlcbdictionaries import *
from CanMessage import *

def manufacturerName(id: int):
    if id in VlcbManufacturer:
        return VlcbManufacturer[id]
    else:
        return f"Unknown({id})"

def moduleName(id: int):
    if id in VlcbMergModuleTypes:
        return VlcbMergModuleTypes[id]
    else:
        return f"Unknown({id})"

def flags(f: int):
    return ' '.join([VlcbParamFlags[bitvalue]
                     for bitvalue in [1 << bit for bit in range(8)]
                     if (f & bitvalue) != 0])

def cpuName(manId: int, cpuId: int):
    if manId == CPUM_MICROCHIP:
        if cpuId in VlcbMicrochipProcessors:
            return VlcbMicrochipProcessors[cpuId]
        else:
            return f"Unknown Microchip processor({cpuId})"
    else:
        return f"Unknown CPU Manufacturer({manId})"


def showCbusMessage(canFrame: CanMessage):
    print(describeCbusMessage(canFrame))

def describeCbusMessage(canFrame: CanMessage):
    op = canFrame.data[0]
    if op == OPC_PNN:
        ret = f"PNN NN={nodeNumber(canFrame.data[1], canFrame.data[2])}" + \
              f" Manufacturer={manufacturerName(canFrame.data[3])}" + \
              f" ModuleID={moduleName(canFrame.data[4])}" + \
              f" Flags={flags(canFrame.data[5])}"
    elif op == OPC_PARAN:
        ret = f"PARAN NN={nodeNumber(canFrame.data[1], canFrame.data[2])}" + \
              f" Parameter no: {canFrame.data[3]}" + \
              f" Parameter value={canFrame.data[4]}"
    elif op == OPC_GRSP:
        ret = f"GRSP NN={nodeNumber(canFrame.data[1], canFrame.data[2])}" + \
              f" Request Op={VlcbOpCodes[canFrame.data[3]]}" + \
              f" Service={VlcbServiceTypes[canFrame.data[4]]}" + \
              f" Result={VlcbGrspCodes[canFrame.data[5]]}"
    elif op == OPC_CMDERR:
        ret = f"CMDERR NN={nodeNumber(canFrame.data[1], canFrame.data[2])}" + \
              f" Result={VlcbCmdErrs[canFrame.data[3]]}"
    elif op == OPC_REVAL:
        ret = f"REVAL NN={nodeNumber(canFrame.data[1], canFrame.data[2])}" + \
              f" Event index={canFrame.data[3]}" + \
              f" Event variable index={canFrame.data[4]}"
    elif op == OPC_NEVAL:
        ret = f"NEVAL NN={nodeNumber(canFrame.data[1], canFrame.data[2])}" + \
              f" Event index={canFrame.data[3]}" + \
              f" EV index={canFrame.data[4]}" + \
              f" Value={canFrame.data[5]}"
    elif op == OPC_ENRSP:
        ret = f"ENRSP NN={nodeNumber(canFrame.data[1], canFrame.data[2])}" + \
              f" Event NN={nodeNumber(canFrame.data[3], canFrame.data[4])}" + \
              f" EN={nodeNumber(canFrame.data[5], canFrame.data[6])}" + \
              f" index={canFrame.data[7]}"
    elif op == OPC_REQEV:
        ret = f"REQEV NN={nodeNumber(canFrame.data[1], canFrame.data[2])}" + \
              f" EN={nodeNumber(canFrame.data[3], canFrame.data[4])}" + \
              f" Event index={canFrame.data[5]}"
    elif op == OPC_EVANS:
        ret = f"EVANS NN={nodeNumber(canFrame.data[1], canFrame.data[2])}" + \
              f" EN={nodeNumber(canFrame.data[3], canFrame.data[4])}" + \
              f" Event index={canFrame.data[5]}" + \
              f" value={canFrame.data[6]}"
    elif op == OPC_ACON or op == OPC_ACOF or op == OPC_ASON or op == OPC_ASOF \
            or op == OPC_AREQ or op == OPC_ARON or op == OPC_AROF \
            or op == OPC_ASRQ or op == OPC_ARSON or op == OPC_ARSOF:
        ret = f"{VlcbOpCodes[op]}" + \
              f" NN={nodeNumber(canFrame.data[1], canFrame.data[2])}" + \
              f" EN={nodeNumber(canFrame.data[3], canFrame.data[4])}"
    elif op == OPC_RQSD:
        ret = f"RQSD NN={nodeNumber(canFrame.data[1], canFrame.data[2])}" + \
              f" Service Index={canFrame.data[3]}"
    elif op == OPC_SD:
        if canFrame.data[3] == 0 and canFrame.data[4] == 0:
            ret = f"SD NN={nodeNumber(canFrame.data[1], canFrame.data[2])}" + \
                  f" Number of Services={canFrame.data[5]}"
        else:
            ret = f"SD NN={nodeNumber(canFrame.data[1], canFrame.data[2])}" + \
                  f" Service Index={canFrame.data[3]}" + \
                  f" Type={VlcbServiceTypes[canFrame.data[4]]}" + \
                  f" Version={canFrame.data[5]}"
    elif op == OPC_ESD:
        ret = f"ESD NN={nodeNumber(canFrame.data[1], canFrame.data[2])}" + \
              f" Service Index={canFrame.data[3]}" + \
              f" Type={VlcbServiceTypes[canFrame.data[4]]}" + \
              f" Data={canFrame.data[5]} {canFrame.data[6]} {canFrame.data[7]}"
    # OP-codes with no data
    elif op == OPC_QNN:
        ret = f"{VlcbOpCodes[op]}"
    # OP-codes with NN and no further data:
    elif op == OPC_RQEVN or op == OPC_WRACK or op == OPC_NERD or op == OPC_NNEVN or op == OPC_NNLRN or op == OPC_NNULN:
        ret = f"{VlcbOpCodes[op]}" + \
              f" NN={nodeNumber(canFrame.data[1], canFrame.data[2])}"
    # OP-codes with NN and a count
    elif op == OPC_NUMEV or op == OPC_EVNLF:
        ret = f"{VlcbOpCodes[op]}" + \
              f" NN={nodeNumber(canFrame.data[1], canFrame.data[2])}" + \
              f" Count={canFrame.data[3]}"
    # OP-codes with NN and an index
    elif op == OPC_RQNPN or op == OPC_NVRD:
        ret = f"{VlcbOpCodes[op]}" + \
              f" NN={nodeNumber(canFrame.data[1], canFrame.data[2])}" + \
              f" index={canFrame.data[3]}"
    # OP-codes with NN and an index and a value
    elif op == OPC_NVSET or op == OPC_NVANS:
        ret = f"{VlcbOpCodes[op]}" + \
              f" NN={nodeNumber(canFrame.data[1], canFrame.data[2])}" + \
              f" index={canFrame.data[3]}" + \
              f" value={canFrame.data[4]}"
    elif op == OPC_RDGN:
        ret = f"RDGN NN={nodeNumber(canFrame.data[1], canFrame.data[2])}" + \
              f" Svc index={canFrame.data[3]}" + \
              f" Diag code={canFrame.data[4]}"
    elif op == OPC_DGN:
        ret = f"DGN NN={nodeNumber(canFrame.data[1], canFrame.data[2])}" + \
              f" Svc index={canFrame.data[3]}" + \
              f" Diag code={canFrame.data[4]}" + \
              f" value={nodeNumber(canFrame.data[5], canFrame.data[6])}"
    elif op == OPC_HEARTB:
        ret = f"HEARTB NN={nodeNumber(canFrame.data[1], canFrame.data[2])}" + \
              f" Seq={canFrame.data[3]}" + \
              f" Status={canFrame.data[4]}" + \
              f" StatusBits={canFrame.data[5]}"
    else:
        ret = f"?? {VlcbOpCodes[canFrame.data[0]]} " + \
              " ".join([f"{b:02X}" for b in canFrame.data[1:canFrame.dlc]])
    expectedLength = (op >> 5) + 1
    if canFrame.dlc != expectedLength:
        ret += f"!! Message length is {canFrame.dlc}, expected {expectedLength}"
    return ret
