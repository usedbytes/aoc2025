import sys

def in_range(x, start, end):
    return x >= start and x <= end

part1 = 0
part2 = 0
with open(sys.argv[1]) as f:
    ranges = f.read().split(",")
    for r in ranges:
        start, end = map(str.strip, r.split("-"))

        start_prefix = start[:len(start) // 2] or 0

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

        # For part 2, build repetitions of increasingly long prefixes
        # This is horrible... I don't have time to fix it!
        max_length = len(end)
        min_length = len(start)
        found = set()
        for ndigits in range(1, (max_length // 2) + 1):
            min_reps = min(min_length // ndigits, max_length // ndigits)
            max_reps = max(min_length // ndigits, max_length // ndigits)
            for reps in range(2, max_reps + 1):
                start_prefix = start[:ndigits]
                i = 1
                while True:
                    v = int(f"{i}" * reps)
                    if v > iend:
                        break

                    if in_range(v, istart, iend) and v not in found:
                        part2 += v
                        found.add(v)
                    i += 1

print(part1)
print(part2)
