import sys

# Just load the input into a transposed grid delimeted by spaces
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

operators = {
    "+": sum,
    "*": product,
}
part1 = 0
for problem in problems:
    part1 += operators[problem[-1]](map(int, problem[:-1]))
print(part1)


# Eric sold us a lie, so part2 is completely different
# load the whole file into a grid and transpose it character-wise
grid = []
with open(sys.argv[1]) as f:
    for line in f:
        grid.append(line.strip("\n"))

part2 = 0
numbers = []
op = None
# Assume all lines are padded
for col in range(len(grid[0])):
    line = ""
    for row in range(len(grid)):
        char = grid[row][col]
        if char in operators:
            op = char
        elif char != " ":
            line += char

    # Line is now either empty (separates problems), or contains
    # a number for the current problem
    if line == "":
        part2 += operators[op](map(int, numbers))
        numbers = []
        op = None
    else:
        numbers.append(line)

# Finish the final problem
part2 += operators[op](map(int, numbers))
print(part2)
