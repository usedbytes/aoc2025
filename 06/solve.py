import sys

ncols = None
with open(sys.argv[1]) as f:
    for line in map(str.strip, f):
        parts = line.split()
        if ncols is None:
            ncols = len(parts)
            problems = [[] for _ in range(ncols)]
        for i, n in enumerate(parts):
            try:
                problems[i].append(int(n))
            except ValueError:
                problems[i].append(n)

def product(vs):
    result = 1
    for v in vs:
        result *= v
    return result

operators = {
    "+": sum,
    "*": product,
}
part1 = 0
for problem in problems:
    part1 += operators[problem[-1]](problem[:-1])
print(part1)
