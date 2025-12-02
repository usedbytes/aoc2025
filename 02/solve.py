import sys

def in_range(x, start, end):
    return x >= start and x <= end

part1 = 0
with open(sys.argv[1]) as f:
    ranges = f.read().split(",")
    for r in ranges:
        start, end = r.split("-")

        start_prefix = start[:len(start)//2] or 0

        istart, iend = int(start), int(end)

        # Build repeated numbers until reaching the end of the range
        i = int(start_prefix)
        while True:
            v = int(f"{i}{i}")
            if v > iend:
                break

            if in_range(v, istart, iend):
                part1 += v
            i += 1

print(part1)
