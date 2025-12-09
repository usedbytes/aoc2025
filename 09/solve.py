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

# Compress the empty space, to make the whole grid manageable
# Smallest "x" value becomes 0, second-smallest becomes 1, etc.
xs = sorted([v[0] for v in tiles])
xmap = {
    original: compressed for compressed, original in enumerate(xs)
}
ys = sorted([v[1] for v in tiles])
ymap = {
    original: compressed for compressed, original in enumerate(ys)
}

compressed_tiles = [
    (xmap[x], ymap[y]) for x, y in tiles
]

max_x, max_y = len(xs), len(ys)

# Make a grid
grid = [
    ["."] * max_x for _ in range(max_y)
]
for i, (x, y) in enumerate(compressed_tiles):
    grid[y][x] = "#"
    # Next point for line segment
    if i < len(compressed_tiles) - 1:
        nx, ny = compressed_tiles[i + 1]
    else:
        nx, ny = compressed_tiles[0]

    # Trace the green lines
    # There will be a more elegant way to do this
    # First handle vertical lines, then horizontal
    dx, dy = nx - x, ny - y
    if dy > 0:
        for gy in range(y+1, ny):
            grid[gy][x] = 'X'
    elif dy < 0:
        for gy in range(y - 1, ny, -1):
            grid[gy][x] = 'X'
    else:
        if dx > 0:
            for gx in range(x+1, nx):
                grid[y][gx] = 'X'
        elif dx < 0:
            for gx in range(x - 1, nx, -1):
                grid[y][gx] = 'X'

# Find a starting point for flood-fill
# We know that the boundary touches the right-hand edge at some point.
# Find a cell with an "X" on the right border, then move one cell left,
# as long as it's empty, we can fill from there.
# This won't work if some input doesn't have a vertical line at the
# right-hand edge (e.g. just red tiles at the right-hand edge)
for y, row in enumerate(grid):
    if row[-1] == "X":
        sx = len(row) - 2
        sy = y
        break
assert grid[sy][sx] == "."

# Flood fill
frontier = [(sx, sy)]
while len(frontier) > 0:
    x, y = frontier.pop()
    grid[y][x] = "X"
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if nx < 0 or nx >= max_x:
                continue
            if ny < 0 or ny >= max_y:
                continue
            nx = x + dx
            ny = y + dy
            if grid[ny][nx] == ".":
                frontier.append((nx, ny))

# For pairs of corners
# Trace the permiter of the rectangle
# If you ever hit a ".", its invalid - this only works because we know the
# region perimeter is one unbroken line.
part2 = 0
for i, (x1, y1) in enumerate(compressed_tiles):
    for j in range(i + 1, len(compressed_tiles)):
        x2, y2 = compressed_tiles[j]
        ok = True
        # Trace the horizontals
        for x in range(x1, x2, -1 if x2 < x1 else 1):
            if grid[y1][x] == "." or grid[y2][x] == ".":
                ok = False
                break
        # Trace the verticals
        for y in range(y1, y2, -1 if y2 < y1 else 1):
            if grid[y][x1] == "." or grid[y][x2] == ".":
                ok = False
                break
        if ok:
            # Unwarp the coords to get the real values
            rx1, rx2 = xs[x1], xs[x2]
            ry1, ry2 = ys[y1], ys[y2]
            a = area((rx1, ry1), (rx2, ry2))
            part2 = max(part2, a)
print(part2)
