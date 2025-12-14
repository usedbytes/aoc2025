import heapq
import sys
from functools import cache

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

def do_line_part2(joltages, buttons):
    # Inspired by https://www.reddit.com/r/adventofcode/comments/1pk87hl/2025_day_10_part_2_bifurcate_your_way_to_victory/

    # First pre-calculate all of the counter values reachable in at-most 1
    # press of each button - these form possible ends to a press sequence
    terminators = {}
    for pressed in range(1 << len(buttons)):
        counts = [0] * len(joltages)
        # Each bit set in 'pressed' is a button to press
        for i in range(pressed.bit_length()):
            if pressed & (1 << i) == 0:
                continue
            button = buttons[i]
            for idx in button:
                counts[idx] += 1
        counts = tuple(counts)
        lsbs = tuple(v & 1 for v in counts)

        # If there are multiple ways to reach the same count, only take the
        # shortest
        # We store the number of presses, and the lsbs to save recalating them
        if counts in terminators:
            terminators[counts] = (min(terminators[counts][0], pressed.bit_count()), lsbs)
        else:
            terminators[counts] = (pressed.bit_count(), lsbs)

    # Now we see which "terminators" are relevant, then recursively
    # reduce the problem by 1/2
    # A terminator is relevant if it reduces the count to an even number
    zero = (0,) * len(joltages)
    @cache
    def do_reduce(counters):
        if counters == zero:
            # Done - no presses
            return 0

        best = 10000
        counters_lsbs = tuple(v & 1 for v in counters)
        for term, (term_count, lsbs) in terminators.items():
            if (lsbs == counters_lsbs and all(c >= term[i] for i, c in enumerate(counters))):
                # Subtract the terminator, then half and recurse
                new_counters = tuple((c - term[i]) // 2 for i, c in enumerate(counters))
                presses = term_count + 2 * do_reduce(new_counters)
                best = min(best, presses)
        return best

    return do_reduce(tuple(joltages))

part1 = 0
part2 = 0
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

        joltages = tuple(map(int, joltage_str[1:-1].split(",")))

        part1 += do_line_part1(target_lights, buttons)

        part2 += do_line_part2(joltages, buttons)
print(part1)
print(part2)
