import sys

def calculate(line, part2 = False):
    ndigits = 12 if part2 else 2
    number = ""
    idx = 0
    for n in range(ndigits):
        # Find the largest up-to the last "tail" digits
        tail = ndigits - n - 1
        # Not sure if there's a better way to make [:-0] work
        if tail > 0:
            sub = line[idx:-(ndigits - n - 1)]
        else:
            sub = line[idx:]
        largest = sorted(sub, reverse=True)[0]
        idx += sub.find(largest) + 1
        number += largest
    return int(number)

part1 = 0
part2 = 0
with open(sys.argv[1]) as f:
    for line in map(str.strip, f):
        part1 += calculate(line)
        part2 += calculate(line, True)
print(part1)
print(part2)
