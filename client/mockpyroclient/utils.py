import math


def convertToNumber(s):
    return int.from_bytes(s.encode(), "little")


def convertFromNumber(n):
    return n.to_bytes(math.ceil(n.bit_length() / 8), "little").decode()
