from canmessage import canmessage

def CANtoGC(self, msg: canmessage.canmessage) -> str:
    tid = msg.canid << 5

    gc = ':'
    gc += f'X{tid:04X}' if msg.ext else f'S{tid:04X}'
    gc += 'R' if msg.rtr else 'N'

    for i in range(msg.dlc):
        gc += f'{msg.data[i]:02X}'

    gc += ';'
    return gc

def GCtoCAN(self, gc: str) -> canmessage.canmessage | None:
    # self.logger.log(f'** GCtoCAN {gc}')
    try:
        msg = canmessage.canmessage()
        msg.ext = True if (gc[1] == 'X') else False
        pos = gc.find('N')

        if pos == -1:
            msg.rtr = True
            pos = gc.find('R')
        else:
            msg.rtr = False

        id = '0X' + gc[2:pos]
        msg.canid = int(id) >> 5

        data = gc[pos + 1: -1]
        msg.dlc = int(len(data) / 2)

        for i in range(msg.dlc):
            j = int(i)
            t = '0x' + data[j * 2: (j * 2) + 2]
            msg.data[i] = int(t)

        # self.logger.log('convert ok')

    except:
        # self.logger.log('** GCtoCAN invalid string')
        msg = None

    return msg