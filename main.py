import os
from protocol_reverse import *
from user_constraints import *
import global_var

global _protocol_config


def read_packet(filepath) -> []:
    file_struct = os.walk(filepath)
    packet_list = []

    for path, dir_list, file_list in file_struct:
        for file_name in file_list:
            if ".bin" in file_name:
                with open(os.path.join(path, file_name), "rb+") as f:
                    packet_list.append(f.read())
    return packet_list


def sort_by_length(packate_list) -> None:
    l = len(packate_list)
    for i in range(l - 1):
        for j in range(i, l):
            l1 = len(packate_list[i])
            l2 = len(packate_list[j])
            if l1 > l2:
                t = packate_list[i]
                packate_list[i] = packate_list[j]
                packate_list[j] = t


def check_lc(packet, lc=None):

    l = len(packet)
    if not lc:
        lc = global_var.get_lc()

    for k in lc:
        if k in global_var.get_fdi():
            continue

        if type(lc) == list:
            if lc[0] == "34-43":
                a = 1

            if type(lc[0]) == str:
                if lc[0] == "A":
                    continue
                b, e = parse_be(lc[0], l)
                if e - b > 10:
                    return lc, k
                continue

            elif type(lc[0]) == dict:
                A, B = check_lc(packet, lc[0])
                if A and B:
                    return A, B
                continue

        # print("-->" + str(lc))
        if type(lc[k]['scope']) == list:
            A, B = check_lc(packet, lc[k]['scope'])
            if A and B:
                return A, B

    return False, False


if __name__ == "__main__":
    global_var.init()

    packet_list = read_packet(r"D:\tool\apr\rdp")
    sort_by_length(packet_list)

    print(packet_list)

    for packet in packet_list:

        _l = len(packet)

        set_packet_len(_l)
        parse_uc(packet)
        get_wall()
        gli = filter_by_length(packet)
        print(gli)
        for idx in gli:
            guess_global_length_constraints(packet, idx)
        _lc, idx = check_lc(packet)
        while idx:

            print("============ {}".format(idx))
            flc = global_var.get_flc()
            flc.append(_lc[0])

            # wall
            b, e = parse_be(_lc[0], _l)
            n = search_wall(b, e)
            release_wall(b, e, n)
            build_wall(0, b, 1)
            build_wall(e, _l, 1)

            get_wall()

            global_var.get_mem().clear()
            gli = filter_by_length(packet, int(b))
            print(gli)
            m = DFS_protocol_analyzes(packet, gli)

            flc.remove(_lc[0])

            build_wall(b, e, n)
            release_wall(0, b, 1)
            release_wall(e, _l, 1)

            if len(m[1]) != 0:
                _lc[0] = m[1]

            print("m[1]=" + str(m[1]))
            print("lc=" + str(global_var.get_lc()))

            _lc, idx = check_lc(packet)
            global_var.get_fdi().append(idx)

        print("======")
        print(global_var.get_lc())