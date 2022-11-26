from utils import *
global uc


def set_packet_len(_l):
    global uc
    uc = {'wall': [0] * _l}


def check_wall(idx, _l, n):

    b = 0
    f = 0

    for i in range(idx, idx + n):
        if uc['wall'][i]:
            return -1

    for i in range(idx + n, idx + _l):
        # print(i)
        if uc['wall'][i] > 0x7fffffff:
            b += 1
            continue

        if uc['wall'][i] < 0x7fffffff and b and not f:
            f = 1
            continue

        # 在找完Type后又出现了Type，因为value是不可切割的，所这里判False
        if uc['wall'][i] > 0x7fffffff and f:
            return -1

        # 在找完Type后出现了wall，所以判False
        if uc['wall'][i] < 0x7fffffff and not b and f:
            return -1

    for i in range(idx + n, idx + _l + b):
        if uc['wall'][i] and uc['wall'][i] < 0x7fffffff:
            return -1
    return b


def parse_be(ss, _l):
    b = int(ss.split("-")[0])
    e = ss.split("-")[1]
    if e == "E":
        e = _l
    else:
        e = int(e)
    return b, e


def release_wall(b, e, n):
    for i in range(b, e):
        uc['wall'][i] -= n


def build_wall(b, e, n):
    for i in range(b, e):
        uc['wall'][i] += n


def parse_uc(packet):
    global uc

    with open("uc.txt", "r+") as f:
        data = f.read().split("\n")

    _l = len(packet)
    for line in data:
        if not line:
            continue
        # print(line)
        ll = line.split(" ")
        b0, e0 = parse_be(ll[0], _l)
        build_wall(b0, e0, 1)

        t = l = -1
        if ll[1] == "L":
            if e0 - b0 == 4:
                l = read4bytes(packet, b0, int(ll[2]))

            if e0 - b0 == 2:
                l = read2bytes(packet, b0, int(ll[2]))

            if e0 - b0 == 1:
                l = read1byte(packet, b0)

            if len(ll) > 3:
                b1, e1 = parse_be(ll[3], _l)
            else:
                b1 = e0
                e1 = e0 + l

            build_wall(b1, e1, 1)
        if ll[1] == "T":
            build_wall(b0, e0, 0xffffffff)


def search_wall(b, e):
    _min = 0xffffffff
    for i in range(b, e):
        if _min > uc['wall'][i]:
            _min = uc['wall'][i]
    return _min


def get_wall():
    print(uc['wall'])



























