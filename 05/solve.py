import sys

def in_range(v, r):
    return v >= r[0] and v <= r[1]

ranges = []
with open(sys.argv[1]) as f:
    for line in f:
        line = line.strip()
        if line == "":
            break

        start, end = line.split("-")
        ranges.append((int(start), int(end)))

    part1 = 0
    for line in f:
        line = line.strip()
        v = int(line)
        for r in ranges:
            if in_range(v, r):
                part1 += 1
                break
print(part1)
