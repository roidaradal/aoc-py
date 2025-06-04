knotHashLimit = 256

def knotHash(lengths: list[int], rounds: int) -> list[int]:
    lengths +=  [17, 31, 73, 47, 23]
    numbers = list(range(knotHashLimit))
    i, skip = 0, 0
    for _ in range(rounds):
        for length in lengths:
            if length > knotHashLimit: continue

            j = i+length
            if j <= knotHashLimit:
                numbers[i:j] = numbers[i:j][::-1] # reverse
            else: # wraparound
                s = knotHashLimit-i
                j = length-s
                chunk = (numbers[i:] + numbers[:j])[::-1]
                numbers[i:] = chunk[:s]
                numbers[:j] = chunk[s:]
            
            i = (i+length+skip) % knotHashLimit 
            skip += 1
    return numbers

def hexCode(x: int) -> str:
    return '%0.2x' % x