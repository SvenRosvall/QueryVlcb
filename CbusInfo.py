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
    op = canFrame.data[0]
    if op == OPC_PNN :
        print("PNN NN=", nodeNumber(canFrame.data[1], canFrame.data[2]),
              " Manufacturer=", manufacturerName(canFrame.data[3]),
              " ModuleID=", moduleName(canFrame.data[4]),
              " Flags=", flags(canFrame.data[5]),
              sep='')
    elif op == OPC_PARAN :
        print("PARAN NN=", nodeNumber(canFrame.data[1], canFrame.data[2]),
              " Parameter no: ", canFrame.data[3],
              " Parameter value=", canFrame.data[4],
              sep='')
    elif op == OPC_GRSP :
        print("GRSP NN=", nodeNumber(canFrame.data[1], canFrame.data[2]),
              " Request Op=", VlcbOpCodes[canFrame.data[3]],
              " Service=", VlcbServiceTypes[canFrame.data[4]],
              " Result=", VlcbGrspCodes[canFrame.data[5]],
              sep='')
    elif op == OPC_CMDERR:
        print("CMDERR NN=", nodeNumber(canFrame.data[1], canFrame.data[2]),
              " Result=", VlcbCmdErrs[canFrame.data[3]],
              sep='')
    elif op == OPC_REVAL:
        print("REVAL NN=", nodeNumber(canFrame.data[1], canFrame.data[2]),
              " Event index=", canFrame.data[3],
              " Event variable index=", canFrame.data[4],
              sep='')
    elif op == OPC_NEVAL:
        print("REVAL NN=", nodeNumber(canFrame.data[1], canFrame.data[2]),
              " Event index=", canFrame.data[3],
              " EV index=", canFrame.data[4],
              " Value=", canFrame.data[5],
              sep='')
    elif op == OPC_ENRSP:
        print ("ENRSP NN=", nodeNumber(canFrame.data[1], canFrame.data[2]),
               " Event NN=", nodeNumber(canFrame.data[3], canFrame.data[4]),
               " EN=", nodeNumber(canFrame.data[5], canFrame.data[6]),
               " index=", canFrame.data[7],
               sep='')
    elif op == OPC_ACON or op == OPC_ACOF or op == OPC_ASON or op == OPC_ASOF\
            or op == OPC_AREQ or op == OPC_ARON or op == OPC_AROF\
            or op == OPC_ASRQ or op == OPC_ARSON or op == OPC_ARSOF:
        print(VlcbOpCodes[op], 
              " NN=", nodeNumber(canFrame.data[1], canFrame.data[2]),
              " EN=", nodeNumber(canFrame.data[3], canFrame.data[4]),
              sep='')
    elif op == OPC_RQSD:
        print ("RQSD NN=", nodeNumber(canFrame.data[1], canFrame.data[2]),
               " Service Index=", canFrame.data[3],
              sep='')
    elif op == OPC_SD:
        if canFrame.data[3] == 0 and canFrame.data[4] == 0:
            print ("SD NN=", nodeNumber(canFrame.data[1], canFrame.data[2]),
                   " Number of Services=", canFrame.data[5],
                  sep='')
        else:
            print ("SD NN=", nodeNumber(canFrame.data[1], canFrame.data[2]),
                   " Service Index=", canFrame.data[3],
                   " Type=", VlcbServiceTypes[canFrame.data[4]],
                   " Version=", canFrame.data[5],
                  sep='')
    elif op == OPC_ESD:
        print ("ESD NN=", nodeNumber(canFrame.data[1], canFrame.data[2]),
               " Service Index=", canFrame.data[3],
               " Type=", VlcbServiceTypes[canFrame.data[4]],
               " Data=", canFrame.data[5], " ", canFrame.data[6], " ", canFrame.data[7], " ",
              sep='')
    # OP-codes with no data
    elif op == OPC_QNN:
        print (VlcbOpCodes[op])
        if canFrame.dlc != 1 :
            print(f"Message length is {canFrame.dlc}, expected 1.")
    # OP-codes with NN and no further data:
    elif op == OPC_RQEVN or op == OPC_WRACK or op == OPC_NERD or op == OPC_NNEVN or op == OPC_NNLRN or op == OPC_NNULN:
        print (VlcbOpCodes[op],
               " NN=", nodeNumber(canFrame.data[1], canFrame.data[2]),
               sep='')
        if canFrame.dlc != 3 :
            print(f"Message length is {canFrame.dlc}, expected 3.")
    # OP-codes with NN and a count
    elif op == OPC_NUMEV or op == OPC_EVNLF:
        print (VlcbOpCodes[op],
               " NN=", nodeNumber(canFrame.data[1], canFrame.data[2]),
               " Count=", canFrame.data[3],
               sep='')
        if canFrame.dlc != 4 :
            print(f"Message length is {canFrame.dlc}, expected 4.")
    # OP-codes with NN and an index
    elif op == OPC_RQNPN or op == OPC_NVRD:
        print (VlcbOpCodes[op],
               " NN=", nodeNumber(canFrame.data[1], canFrame.data[2]),
               " index=", canFrame.data[3],
               sep='')
        if canFrame.dlc != 4 :
            print(f"Message length is {canFrame.dlc}, expected 4.")
    # OP-codes with NN and an index and a value
    elif op == OPC_NVSET or op == OPC_NVANS:
        print (VlcbOpCodes[op],
               " NN=", nodeNumber(canFrame.data[1], canFrame.data[2]),
               " index=", canFrame.data[3],
               " value=", canFrame.data[4],
               sep='')
        if canFrame.dlc != 5 :
            print(f"Message length is {canFrame.dlc}, expected 5.")
    # Other op: RDGN, DGN
    else:
        print("??", VlcbOpCodes[canFrame.data[0]], end='')
        for i in range(1, canFrame.dlc):
            print(f" {canFrame.data[i]:02X}", end='')
        print()

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
        result[svc.data[4]] = svc.data[3]
    return result

def findServiceIndex(cbusConnection, nn, svcType) -> int:
    return findServiceIndices(cbusConnection, nn)[svcType]

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
    return value
