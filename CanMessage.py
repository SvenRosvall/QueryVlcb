

def nodeNumber(h: int, l:int):
    return (h<<8) + l

def hibyte(n: int) -> int:
    return n >> 8

def lobyte(n: int) -> int:
    return n & 0xFF

class CanMessage:
    def __init__(self,
                 canid: int = 0,
                 dlc: int = -1,
                 op_code: int = -1,
                 node_number: int = -1,
                 data = None,
                 rtr: bool = False,
                 ext: bool = False):
        # if data is None:
        #     data = []
        self.canid = canid
        self.make_header()
        self.dlc = dlc
        self.rtr = rtr
        self.ext = ext
        if data is not None:
            #print("New CanMessage with user provided data: ", data)
            self.data = bytearray(data)
            datalen = len(data)
        else:
            #print("New CanMessage without data")
            self.data = bytearray(8)
            datalen = 0
        #print("CanMessage data len=", datalen, "data=", self.data)
        if op_code >= 0:
            self.data[0] = op_code
            datalen = max(datalen, 1)
            #print(f"CanMessage set opc={op_code}, new len={datalen}")
        if node_number >= 0:
            self.data[1] = hibyte(node_number)
            self.data[2] = lobyte(node_number)
            datalen = max(datalen, 3)            
        if self.dlc == -1:
            self.dlc = datalen
            #print("CanMessage dlc not set, setting to", self.dlc)
        if self.data is not None and datalen > 0 and datalen != (self.data[0] >> 5) + 1:
            raise ValueError(f"Incorrect number of data bytes ({datalen}) for opcode {self.data[0]:X}")

    def __str__(self):
        rtr = "R" if self.rtr else ""
        ext = "X" if self.ext else ""
        cstr = (
                f"[{self.canid:x}] "
                + f"[{self.dlc:x}] [ "
                + " ".join("{:02x}".format(x) for x in self.data[:self.dlc])
                + " ] "
                + rtr
                + ext
        )
        return cstr

    def make_header(self, priority=0x0b) -> None:
        self.canid = (priority << 7) + (self.canid & 0x7f)

    def get_canid(self) -> int:
        return self.canid & 0x7f

    def get_op_code(self) -> int:
        return self.data[0]

    def get_node_number(self) -> int:
        return (self.data[1] << 8) + (self.data[2] & 0xff)

    def get_event_number(self) -> int:
        return (self.data[3] << 8) + (self.data[4] & 0xff)

    def get_node_and_event_numbers(self) -> tuple:
        return self.get_node_number(), self.get_event_number(),

    def print(self, hex_fmt=True) -> None:
        rtr = "R" if self.rtr else ""
        ext = "X" if self.ext else ""

        if hex_fmt:
            byteFormat="{:02X}"
        else:
            byteFormat="{:02}"
        print(
            f"[{self.canid:x}] [{self.dlc:x}] "
            + "[ "
            + " ".join(byteFormat.format(x) for x in self.data[:self.dlc])
            + " ] "
            + rtr
            + ext
        )
