import sys

pos = 50
part1 = 0
N_POS = 100
dirs = {
    "L": -1,
    "R": 1,
}

with open(sys.argv[1]) as f:
    for line in map(str.strip, f):
        d = dirs[line[0]]
        n = int(line[1:])

        pos += d * n
        pos = pos % N_POS

        if pos == 0:
            part1 += 1
print(part1)
