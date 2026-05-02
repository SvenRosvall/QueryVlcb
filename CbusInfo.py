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

NodeNumberDef = {
    "bytes": 2,
    "name": "NN"
}
EventNumberDef = {
    "bytes": 2,
    "name": "EN"
}
EventIndexDef = {
    "bytes": 1,
    "name": "Event Index"
}
EventValueDef = {
    "bytes": 1,
    "name": "Value"
}
ServiceIndexDef = {
    "bytes": 1,
    "name": "Service Index"
}
ServiceTypeDef = {
    "bytes": 1,
    "value": lambda v: VlcbServiceTypes[v],
    "name": "Service Type"
}

VlcbOpCodeDefs = {
    OPC_GRSP: {
        "params": [ 
            NodeNumberDef,
            { 
                "bytes": 1,
                "name": "Request Op",
                "value": lambda v: VlcbOpCodes[v]
            },
            ServiceTypeDef,
            {
                "bytes": 1,
                "name": "Result",
                "value": lambda v: VlcbGrspCodes[v]
            }
        ]
    },
    OPC_CMDERR: {
        "params": [
            NodeNumberDef,
            {
                "bytes": 1,
                "name": "Result",
                "value": lambda v: VlcbCmdErrs[v]
            }
        ]
    },
    OPC_QNN: {
        "params": [],
        "description": "Query for online nodes"
    },
    OPC_PNN: {
        "params": [
            NodeNumberDef,
            {
                "bytes": 1,
                "name": "Manufacturer",
                "value": lambda v : manufacturerName(v)
            },
            {
                "bytes": 1,
                "name": "ModuleID",
                "value": lambda v : moduleName(v)
            },
            {
                "bytes": 1,
                "name": "Flags",
                "value": lambda v : flags(v)
            }
        ],
        "description": "Response to QNN with node details"
    },
    OPC_PARAN: {
        "params": [
            NodeNumberDef,
            {
                "bytes": 1,
                "name": "Parameter no"
            },
            {
                "bytes": 1,
                "name": "Parameter value"
            }
        ]
    },
    OPC_RQSD: {
        "params": [ NodeNumberDef, ServiceIndexDef ],
        "description": "Request Service Discovery"
    },
    OPC_SD: {
        "alt_params": {
            "cond": lambda msg : "count" if msg[3] == 0 and msg[4] == 0 else "service",
            "count": [
                NodeNumberDef,
                { "ignore": 2 },
                { "bytes": 1, "name": "Number of Services" }
            ],
            "service": [
                NodeNumberDef,
                ServiceIndexDef,
                ServiceTypeDef,
                { "bytes": 1, "name": "Version" }
            ]
        },
        "description": "Response to service discovery request"
    },
    OPC_ESD: {
        "params": [
            NodeNumberDef,
            ServiceIndexDef,
            ServiceTypeDef,
            { "bytes": 1, "name": "Data1" },
            { "bytes": 1, "name": "Data2" },
            { "bytes": 1, "name": "Data3" }
        ],
        "description": "Extended response to service discovery request"
    },
    OPC_EVANS: { 
        "params": [ NodeNumberDef, EventNumberDef, EventIndexDef, EventValueDef ],
        "description": "Response to a request event variable in learn mode" 
    },
    OPC_ACON: {
        "params": [ NodeNumberDef, EventNumberDef ],
        "description": "Long Event ON"
    },
    OPC_ACOF: {
        "params": [ NodeNumberDef, EventNumberDef ],
        "description": "Long Event OFF"
    },
    OPC_ASON: {
        "params": [ NodeNumberDef, EventNumberDef ],
        "description": "Short Event ON"
    },
    OPC_ASOF: {
        "params": [ NodeNumberDef, EventNumberDef ],
        "description": "Short Event OFF"
    },
    OPC_AREQ: {
        "params": [ NodeNumberDef, EventNumberDef ],
        "description": "Request Long Event State"
    },
    OPC_ARON: {
        "params": [ NodeNumberDef, EventNumberDef ],
        "description": "Response Long Event ON"
    },
    OPC_AROF: {
        "params": [ NodeNumberDef, EventNumberDef ],
        "description": "Response Long Event OFF"
    },
    OPC_ASRQ: {
        "params": [ NodeNumberDef, EventNumberDef ],
        "description": "Request Short Event State"
    },
    OPC_ARSON: {
        "params": [ NodeNumberDef, EventNumberDef ],
        "description": "Response Short Event ON"
    },
    OPC_ARSOF: {
        "params": [ NodeNumberDef, EventNumberDef ],
        "description": "Response Short Event OFF"
    }
}

def getValue(data, start, count) :
    ret = 0
    for i in range(count):
        ret *= 256
        ret += data[start + i]
    return ret

def describeCbusMessage(canFrame: CanMessage):
    op = canFrame.data[0]
    #print(f"Describing message : {canFrame}")
    if (op in VlcbOpCodeDefs):
        opDef = VlcbOpCodeDefs[op]
        ret = VlcbOpCodes[op]
        if "alt_params" in opDef:
            alt_key = opDef["alt_params"]["cond"](canFrame.data)
            params = opDef["alt_params"][alt_key]
        else:
            params = opDef["params"]
        i = 1
        for d in params:
            if "ignore" in d:
                i += d["ignore"]
                continue
            value = getValue(canFrame.data, i, d["bytes"])
            if ("value" in d):
                value = d["value"](value)
            ret += f" {d["name"]}={value}"
            i += d["bytes"]
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
