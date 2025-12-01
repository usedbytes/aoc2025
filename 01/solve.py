import sys

pos = 50
part1 = 0
part2 = 0
N_POS = 100
dirs = {
    "L": -1,
    "R": 1,
}

with open(sys.argv[1]) as f:
    for line in map(str.strip, f):
        d = dirs[line[0]]
        n = int(line[1:])

        clicks = d * n
        full_rots = abs(clicks) // N_POS
        mod = abs(clicks) % N_POS

        # The "pos != 0" clause is a little messy here, there might
        # be a neater way
        if d < 0 and pos != 0 and mod >= pos:
            part2 += 1
        elif d > 0 and pos != 0 and mod >= (N_POS - pos):
            part2 += 1
        part2 += full_rots

        pos += clicks
        pos = pos % N_POS
        if pos == 0:
            part1 += 1
print(part1)
print(part2)
