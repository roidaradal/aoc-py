# Advent of Code 2019 Day 08
# John Roy Daradal 

from aoc import *

dims = (6,25)

def data(full: bool) -> list[str]:
    line = readFirstLine(19, 8, full)
    h,w = dims 
    layer = h*w
    img = []
    for i in range(0, len(line), layer):
        img.append(line[i:i+layer])
    return img

def solve() -> Solution:
    layers = data(full=True)

    # Part 1
    freq = {i: charFreq(layer) for i,layer in enumerate(layers)}
    min0 = min((f['0'],i) for i,f in freq.items())[1]
    f = freq[min0]
    part1 = f['1'] * f['2']

    # Part 2
    h,w = dims 
    img = []
    for i in range(h*w):
        for layer in layers:
            if layer[i] != '2':
                img.append(layer[i])
                break 
    # render 
    T = {'1': '#', '0': ' '}
    for i in range(0, len(img), w):
        row = [T[x] for x in img[i:i+w]]
        print(''.join(row)) 

    return newSolution(part1, "")

if __name__ == '__main__':
    do(solve, 19, 8)

'''
Part1:
- Compute the character frequency for each layer 
- Find the layer with the fewest 0 digits (min0)
- Output the product of no. of 1s and no. of 2s in that layer

Part2:
- For each pixel, go through the layers to find the rendered color
- Skip 2s as they are transparent; stop going through layers once we find a non-2 value
- Render the image by displaying 1s as # and 0s a blank
- Since the image layer is layed out as one string, divide it into width chunks
'''