from utils import *
from user_constraints import *
import global_var


def guess_total_length(packet, _l, idx, bl):
    length_constraints = global_var.get_lc()
    l = len(packet)

    if _l == l:
        length_constraints[idx] = {}
        length_constraints[idx]['scope'] = ["A"]
        length_constraints[idx]['bytes'] = bl
        return 1
    return 0


def guess_remaining_length(packet, _l, idx, bl):
    length_constraints = global_var.get_lc()
    l = len(packet)
    if _l == l - idx - bl:
        length_constraints[idx] = {}
        length_constraints[idx]['scope'] = [str(idx + bl) + "-E"]
        length_constraints[idx]['bytes'] = bl
        return 1
    return 0


def guess_global_length_constraints(packet, idx):
    # 4 bytes
    ll = read4bytes(packet, idx, 0)
    if guess_total_length(packet, ll, idx, 4) or guess_remaining_length(packet, ll, idx, 4):
        return 1
    bl = read4bytes(packet, idx, 1)
    if guess_total_length(packet, bl, idx, 4) or guess_remaining_length(packet, bl, idx, 4):
        return 1

    # 2 bytes
    ll = read2bytes(packet, idx, 0)
    if guess_total_length(packet, ll, idx, 2) or guess_remaining_length(packet, ll, idx, 2):
        return 1
    bl = read2bytes(packet, idx, 1)
    if guess_total_length(packet, bl, idx, 2) or guess_remaining_length(packet, bl, idx, 2):
        return 1

    # 1 byte
    _l = read1byte(packet, idx)
    if guess_total_length(packet, _l, idx, 1) or guess_remaining_length(packet, _l, idx, 1):
        return 1

    return 0


def quick_search_by_mem(idx):
    mem = global_var.get_mem()
    for m in mem:
        if idx == m['begin_idx']:
            return m
    return 0


def DFS_sub_search(packet, idx, consume_len, bytes_len):
    gli = filter_by_length(packet, idx + consume_len)
    r, _lc = DFS_protocol_analyzes(packet, gli)
    r = r + consume_len
    lc = str(idx + bytes_len) + "-" + str(idx + consume_len)
    if not _lc:
        m = {'begin_idx': idx, 'lc': {idx: {"scope": [lc], "bytes": bytes_len}}, 'calc_bytes': r}
    else:
        _ = D_deep_copy(_lc)

        if idx not in _:
            _[idx] = {"scope": [], "bytes": bytes_len}
        _[idx]['scope'].append(lc)
        m = {'begin_idx': idx, 'lc': _, 'calc_bytes': r}

    return m['calc_bytes'], m


def DFS_protocol_analyzes(packet, guess_length_idx):
    l = len(packet)

    if len(guess_length_idx) == 0:
        return 0, []

    current_frame_m = None
    for idx in guess_length_idx:

        if idx == 23:
            a = 1

        r0 = r1 = r2 = r3 = r4 = -1

        m = quick_search_by_mem(idx)
        if not m:
            bl4 = read4bytes(packet, idx, 1)
            if bl4 <= l - idx - 4:
                T = check_wall(idx, bl4 + 4, 4)
                if T != -1 and bl4 <= l - idx - 4 - T:
                    r0, m0 = DFS_sub_search(packet, idx + T, bl4 + 4, 4)

            ll4 = read4bytes(packet, idx, 0)
            if ll4 <= l - idx - 4:
                T = check_wall(idx, ll4 + 4, 4)
                if T != -1 and ll4 <= l - idx - 4 - T:
                    r1, m1 = DFS_sub_search(packet, idx + T, ll4 + 4, 4)

            bl2 = read2bytes(packet, idx, 1)
            if bl2 <= l - idx - 2:
                T = check_wall(idx, bl2 + 2, 2)
                if T != -1 and bl2 <= l - idx - 2 - T:
                    r2, m2 = DFS_sub_search(packet, idx + T, bl2 + 2, 2)

            ll2 = read2bytes(packet, idx, 0)
            if ll2 <= l - idx - 2:
                T = check_wall(idx, ll2 + 2, 2)
                if T != -1 and ll2 <= l - idx - 2 - T:
                    r3, m3 = DFS_sub_search(packet, idx + T, ll2 + 2, 2)

            _l = read1byte(packet, idx)
            if _l <= l - idx - 1:
                T = check_wall(idx, _l + 1, 1)
                if T != -1 and _l <= l - idx - 1 - T:
                    r4, m4 = DFS_sub_search(packet, idx + T, _l + 1, 1)

            r = who_is_max(r0, r1, r2, r3, r4)
            mem = global_var.get_mem()

            _find = 0
            m = {}
            if len(r) != 0:
                m = eval(r.split(',')[1])
            for _m in mem:
                if idx == _m['begin_idx']:
                    if len(r) != 0:
                        if m['calc_bytes'] > _m['calc_bytes']:
                            _m['lc'] = m['lc']
                            _m['calc_bytes'] = m['calc_bytes']
                    else:
                        _m['lc'] = []
                        _m['calc_bytes'] = 0
                    _find = 1
                    break
            if not _find:
                if len(r) != 0:
                    mem.append({'begin_idx': idx, 'lc': m['lc'], 'calc_bytes': m['calc_bytes']})
                else:
                    mem.append({'begin_idx': idx, 'lc': [], 'calc_bytes': 0})
                # print("update=" + str(global_var.get_mem()))

        if m:
            if current_frame_m:
                if m['calc_bytes'] > current_frame_m['calc_bytes']:
                    current_frame_m = m
            else:
                current_frame_m = m

    if current_frame_m:
        # print("current_frame_m=" + str(current_frame_m))
        return current_frame_m['calc_bytes'], current_frame_m['lc']
    else:
        return 0, []
