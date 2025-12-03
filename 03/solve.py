import sys

part1 = 0
with open(sys.argv[1]) as f:
    for line in map(str.strip, f):
        largest = sorted(line[:-1], reverse=True)[0]
        idx = line.find(largest)
        second = sorted(line[idx+1:], reverse=True)[0]
        number = int(largest + second)

        part1 += number
print(part1)
