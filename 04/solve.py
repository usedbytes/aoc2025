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

removable = set()

def count_adjacent(roll):
    row, col = roll
    nrolls = 0
    for dr, dc in adjacent:
        if (row + dr, col + dc) in grid:
            nrolls += 1
    return nrolls

for roll in grid:
    nrolls = count_adjacent(roll)
    if nrolls < 4:
        removable.add(roll)

# Part 1
print(len(removable))

# Now start removing... Not elegantly
part2 = 0
while len(removable) > 0:
    roll = removable.pop()
    grid.remove(roll)
    part2 += 1

    row, col = roll
    # Re-evaluate all neighbours
    for dr, dc in adjacent:
        new_roll = (row + dr, col + dc)
        if new_roll in grid:
            nrolls = count_adjacent(new_roll)
            if nrolls < 4:
                removable.add(new_roll)
# Part 2
print(part2)
