import heapq
import sys

from collections import defaultdict

boxes = []
with open(sys.argv[1]) as f:
    for line in map(str.strip, f):
        x, y, z = map(int, line.split(","))
        boxes.append((x, y, z))

# Skip the sqrt...
def distance(a, b):
    return (a[0] - b[0])**2 + (a[1] - b[1])**2 + (a[2] - b[2])**2

distances = []
seen = set()
for i, a in enumerate(boxes):
    for ii, b in enumerate(boxes[i:]):
        j = i + ii
        if i == j:
            continue
        d = distance(a, b)
        heapq.heappush(distances, (d, i, j))

circuits = [
    set([x]) for x in range(len(boxes))
]
circuit_idxs = {
    x: x for x in range(len(boxes))
}

NCONNS = 10 if len(boxes) < 1000 else 1000
i = 0
while True:
    if i == NCONNS:
        sizes = sorted(map(len, circuits), reverse=True)
        part1 = sizes[0] * sizes[1] * sizes[2]
        print(part1)

    i += 1

    _, a, b = heapq.heappop(distances)
    ac = circuits[circuit_idxs[a]]
    bc = circuits[circuit_idxs[b]]

    if ac is bc:
        continue

    # Merge them, remove all references to bc, and wipe it
    ac.update(bc)
    for c in bc:
        circuit_idxs[c] = circuit_idxs[a]
    bc.clear()

    if len(ac) == len(boxes):
        part2 = boxes[a][0] * boxes[b][0]
        print(part2)
        break
