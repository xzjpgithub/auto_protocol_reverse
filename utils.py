import global_var


def read4bytes(A, idx, endian):
    try:
        if endian == 0:
            return A[idx] + (A[idx + 1] << 8) + (A[idx + 2] << 16) + (A[idx + 3] << 24)
        if endian == 1:
            return (A[idx] << 24) + (A[idx + 1] << 16) + (A[idx + 2] << 8) + A[idx + 3]
    except IndexError as e:
        return -1


def read2bytes(A, idx, endian):
    try:
        if endian == 0:
            return A[idx] + (A[idx + 1] << 8)
        if endian == 1:
            return (A[idx] << 8) + A[idx + 1]
    except IndexError as e:
        return -1


def read1byte(A, idx):
    return A[idx]


def A_deep_copy(A):
    B = []
    if A:
        for c in A:
            B.append(c)
    return B


def D_deep_copy(D):
    B = {}

    for c in D:
        B[c] = D[c]
    return B


def check_flc(idx):
    flc = global_var.get_flc()

    if len(flc) == 0:
        return True

    f = 1

    for c in flc:
        b = c.split("-")[0]
        e = c.split("-")[1]

        if b == "E":
            continue

        b = int(b)
        if e == "E" and idx >= b:
            continue

        e = int(e)
        if b <= idx <= e:
            continue

        f = 0
        break

    if f:
        return True

    return False


def filter_by_length(packet, begin=0) -> []:
    l = len(packet)
    guess_length_idx = []

    for i in range(begin, l):
        if not check_flc(i):
            continue
        if l < 255:
            if 0 < packet[i] <= l:
                guess_length_idx.append(i)
        else:
            if i <= l - 2:
                if 0 < ((packet[i] << 8) + packet[i + 1]) <= l or \
                        0 < ((packet[i + 1] << 8) + packet[i]) <= l or \
                        0 < packet[i] <= l - i:
                    guess_length_idx.append(i)
    return guess_length_idx


def who_is_max(r0, r1, r2, r3, r4):

    if r0 > r1 and r0 > r2 and r0 > r3 and r0 > r4:
        return "r0, m0"
    if r1 > r0 and r1 > r2 and r1 > r3 and r1 > r4:
        return "r1, m1"
    if r2 > r1 and r2 > r0 and r2 > r3 and r2 > r4:
        return "r2, m2"
    if r3 > r1 and r3 > r2 and r3 > r0 and r3 > r4:
        return "r3, m3"
    if r4 > r1 and r4 > r2 and r4 > r3 and r4 > r0:
        return "r4, m4"

    return ""