
def binary(integer):
    r = bin(integer)
    return r[2:]


def bin2str(message: str, length: int = 8) -> str:
    r = ''
    for i in range(0, len(message), length):
        r += chr(int(message[i:i+length], 2))
    return r

def str2bin(message: str, length: int = 8) -> str:
    r = ''
    for char in message:
        c = bin(ord(char))[2:]
        if len(r) != length:
            c = '0'*(length - len(r)) + c
        assert len(c) == length
        r += c
    return r
