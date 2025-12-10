import heapq
import sys

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
        buttons_lights = []
        for b in buttons_strs:
            toggles = 0
            for v in map(int, b[1:-1].split(",")):
                toggles |= (1 << v)
            buttons_lights.append(toggles)

        # Do a BFS, keep applying XOR until you reach
        # the solution

        heap = []
        # Initial state is we push each button once
        # Heap stores (pushes, state)
        for b in buttons_lights:
            heapq.heappush(heap, (1, b))

        # No point in revisiting the same states
        seen = set()
        while True:
            pushes, state = heapq.heappop(heap)
            if state == target_lights:
                part1 += pushes
                break

            if state in seen:
                continue

            seen.add(state)
            for b in buttons_lights:
                heapq.heappush(heap, (pushes + 1, state ^ b))
print(part1)
