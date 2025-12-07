import sys

part1 = 0
with open(sys.argv[1]) as f:
    wave = set()
    for line in map(str.strip, f):
        if "S" in line:
            wave.add(line.find("S"))
            continue

        # We can't mutate a set while iterating, so create a new
        # wavefront at each step
        new_wave = set(wave)
        for idx in wave:
            if line[idx] == "^":
                part1 += 1
                new_wave.remove(idx)
                new_wave.add(idx - 1)
                new_wave.add(idx + 1)
        wave = new_wave
print(part1)
