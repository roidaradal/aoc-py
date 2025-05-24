# IntCode Common Functions
# John Roy Daradal

def modes(cmd: str, count: int) -> list[int]: 
    m = [0] * count
    if len(cmd) == 0: return m

    i = 0
    for x in reversed(cmd):
        m[i] = int(x)
        i += 1
    return m

def param(x: int, mode: int, numbers: list[int]) -> int:
    return numbers[x] if mode == 0 else x

def param2(x: int, mode: int, rbase: int, numbers: dict[int,int]) -> int:
    if mode in (0,2):
        idx = index(x, mode, rbase)
        return numbers[idx]
    elif mode == 1:
        return x 
    return 0

def index(x: int, mode: int, rbase: int) -> int:
    idx = x 
    if mode == 2: idx += rbase 
    return idx