import heapq
import sys

def do_line_part1(target, buttons):
    # Do a BFS, keep applying XOR until you reach
    # the solution

    toggles = []
    for b in buttons:
        mask = 0
        for v in b:
            mask |= (1 << v)
        toggles.append(mask)

    heap = []
    # Initial state is we push each button once
    # Heap stores (pushes, state)
    for mask in toggles:
        heapq.heappush(heap, (1, mask))

    # No point in revisiting the same states
    seen = set()
    while True:
        pushes, state = heapq.heappop(heap)
        if state == target:
            return pushes

        if state in seen:
            continue

        seen.add(state)
        for mask in toggles:
            heapq.heappush(heap, (pushes + 1, state ^ mask))

part1 = 0
with open(sys.argv[1]) as f:
    for n, line in enumerate(map(str.strip, f)):
        lights_str, *buttons_strs, joltage_str = line.split(" ")

        # Make bitmask of the target light state
        target_lights = 0
        for i, c in enumerate(lights_str[1:-1]):
            if c == '#':
                target_lights |= (1 << i)

        # Bitmasks per button of the toggled lights
        buttons = []
        for b in buttons_strs:
            buttons.append(tuple(map(int, b[1:-1].split(","))))

        part1 += do_line_part1(target_lights, buttons)
print(part1)
