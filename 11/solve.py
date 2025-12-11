import sys
from functools import cache

conns = {}
with open(sys.argv[1]) as f:
    for line in map(str.strip, f):
        output, inputs = line.split(": ")
        inputs = inputs.split(" ")

        assert output not in conns
        conns[output] = inputs

# Assume there are no loops, and do a simple DFS
@cache
def search_p1(start):
    ins = conns[start]
    paths = 0
    for i in ins:
        if i == "out":
            paths += 1
        else:
            paths += search_p1(i)
    return paths

part1 = search_p1("you")
print(part1)

# Just hard-coding two parameters is easier than messing around
# with a cacheable datastructure and copying it
@cache
def search_p2(start, fft, dac):
    ins = conns[start]
    paths = 0

    if start == "fft":
        fft = True
    if start == "dac":
        dac = True

    for i in ins:
        if i == "out":
            if (fft and dac):
                paths += 1
        else:
            paths += search_p2(i, fft, dac)
    return paths

part2 = search_p2("svr", False, False)
print(part2)
