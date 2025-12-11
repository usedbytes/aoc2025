import sys

conns = {}
with open(sys.argv[1]) as f:
    for line in map(str.strip, f):
        output, inputs = line.split(": ")
        inputs = inputs.split(" ")

        assert output not in conns
        conns[output] = inputs

# Assume there are no loops, and do a simple DFS
# Could add @cache if needed
def search(start):
    ins = conns[start]
    paths = 0
    for i in ins:
        if i == "out":
            paths += 1
        else:
            paths += search(i)
    return paths

part1 = search("you")
print(part1)
