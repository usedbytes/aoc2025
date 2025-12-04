import sys

with open(sys.argv[1]) as f:
    grid = set()
    for row, line in enumerate(map(str.strip, f)):
        for col, char in enumerate(line):
            if char == "@":
                grid.add((col, row))

nrows = row + 1
ncols = col + 1

adjacent = [
    (-1, -1),
    ( 0, -1),
    ( 1, -1),
    (-1,  0),
    ( 1,  0),
    (-1,  1),
    ( 0,  1),
    ( 1,  1),
]

part1 = 0
for (row, col) in grid:
    nrolls = 0
    for dr, dc in adjacent:
        if (row + dr, col + dc) in grid:
            nrolls += 1
    if nrolls < 4:
        part1 += 1

print(part1)
