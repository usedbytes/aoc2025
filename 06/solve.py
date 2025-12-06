import sys

# Just load the input into a transposed grid
ncols = None
with open(sys.argv[1]) as f:
    for line in map(str.strip, f):
        parts = line.split()
        if ncols is None:
            ncols = len(parts)
            problems = [[] for _ in range(ncols)]
        for i, n in enumerate(parts):
                problems[i].append(n)

def product(vs):
    result = 1
    for v in vs:
        result *= v
    return result

operations = {
    "+": sum,
    "*": product,
}
part1 = 0
for problem in problems:
    part1 += operations[problem[-1]](map(int, problem[:-1]))
print(part1)


# Eric sold us a lie, so part2 is completely different - load the whole file
# into a grid, use the operators to find the columns.
grid = []
with open(sys.argv[1]) as f:
    for line in f:
        grid.append(line.strip("\n"))

def find_operators(line):
    operators = []
    for i, c in enumerate(line):
        if c != " ":
            operators.append((i, c))
    operators.append((len(line) + 1, ""))

    return operators

operators = find_operators(grid[-1])

part2 = 0
for i, (start, op) in enumerate(operators[:-1]):
    end = operators[i+1][0]
    numbers = ["" for _ in range(end - start - 1)]
    for row in grid[:-1]:
        for n, col in enumerate(range(start, end - 1)):
            c = row[col]
            if c != " ":
                numbers[n] += c
    part2 += operations[op](map(int, numbers))
print(part2)
