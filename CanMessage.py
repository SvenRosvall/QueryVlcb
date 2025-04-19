from vlcbdictionaries import VlcbOpCodes


class CanMessage:
    def __init__(self,
                 canid: int = 0,
                 dlc: int = -1,
                 op_code: int = -1,
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

    def __iter__(self):
        if self.dlc > 0:
            if self.is_event():
                self.polarity = 0 if self.data[0] & 1 else 1
                for x in self.polarity, self.get_node_number(), self.get_event_number():
                    yield x
            else:
                for x in self.data[:self.dlc]:
                    yield x

    def make_header(self, priority=0x0b) -> None:
        self.canid = (priority << 7) + (self.canid & 0x7f)

    def get_canid(self) -> int:
        return self.canid & 0x7f

    def is_event(self) -> bool:
        return self.data[0] in VlcbOpCodes

    def is_short_event(self) -> bool:
        return True if self.is_event() and self.data[0] & (1 << 3) else False

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
