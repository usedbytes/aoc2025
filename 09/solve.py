import sys

tiles = []
with open(sys.argv[1]) as f:
    for line in map(str.strip, f):
        x, y = map(int, line.split(","))
        tiles.append((x, y))

def area(a, b):
    return (abs(a[0] - b[0]) + 1) * (abs(a[1] - b[1]) + 1)

part1 = 0
for i in range(len(tiles)):
    for j in range(i+1, len(tiles)):
        a, b = tiles[i], tiles[j]
        part1 = max(part1, area(a, b))
print(part1)
