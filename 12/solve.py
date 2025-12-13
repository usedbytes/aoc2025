from collections import namedtuple
import heapq
import sys

# Vague plan:
# 1. Parse input shapes into arrays of integers, one per line. '1' for '#'
#   - Shape has list of rows: [(row_mask, n_ones, n_zeros), ...]
# 2. Calculate rotates/flips for each shape (8 variants)
#   - R0
#   - R90: Right column first
#   - R270: Left column upwards first
#   - R180: Bottom row backwards
#   - HFLIP for each: iterate each row backwards
# 3. Deduplicate the shapes (some are symmetric)
# 4. Shapes is a flat list, but each remembers which id (group) it is
# 5. Build the grid - just a list of integers (all 0)
# 6. Start at offset (0,0)
# 7. Try each shape in turn:
#     - AND mask with grid, check for collision
#     - If no collision, calculate a score: number of zeroes removed within the
#       current ROI
# 8. Pick the best score - place shape, update ROI, subtract from pool count
# 9. Move to next offset
# BUT I don't know how we can be sure in the case of failures - do we need to
# try all permutations?

Shape = namedtuple("Shape", "dims, group, masks, n_ones, n_zeroes")
Region = namedtuple("Region", "dims, counts")

def transform_shape(shape):
    # Lazy.
    assert shape.dims == (3, 3)

    seen = set()
    seen.add(shape.masks)

    # R90
    masks = []
    for x in [2, 1, 0]:
        mask = 0
        for out_bit, y in enumerate([0, 1, 2]):
            b = ((shape.masks[y] >> x) & 1)
            mask |= ((shape.masks[y] >> x) & 1) << out_bit
        masks.append(mask)
    seen.add(tuple(masks))

    # R180
    masks = []
    for y in [2, 1, 0]:
        mask = 0
        for out_bit, x in enumerate([2, 1, 0]):
            mask |= ((shape.masks[y] >> x) & 1) << out_bit
        masks.append(mask)
    seen.add(tuple(masks))

    ## R270
    masks = []
    for x in [0, 1, 2]:
        mask = 0
        for out_bit, y in enumerate([2, 1, 0]):
            mask |= ((shape.masks[y] >> x) & 1) << out_bit
        masks.append(mask)
    seen.add(tuple(masks))

    # Then hflip them all
    seen_flipped = set()
    for i, masks in enumerate(seen):
        flipped = []
        for y in [0, 1, 2]:
            mask = 0
            for out_bit, x in enumerate([2, 1, 0]):
                mask |= ((masks[y] >> x) & 1) << out_bit
            flipped.append(mask)
        seen_flipped.add(tuple(flipped))
    seen.update(seen_flipped)

    # Finally, make new shapes
    dims = shape.dims
    shapes = []
    for masks in seen:
        n_ones = []
        n_zeroes = []
        # XXX: If they weren't square, we'd need to know to swap w/h
        for r in masks:
            n_ones.append(r.bit_count())
            n_zeroes.append(shape.dims[0] - r.bit_count())
        new_shape = Shape(shape.dims, shape.group, tuple(masks), tuple(n_ones), tuple(n_zeroes))
        shapes.append(new_shape)
    return shapes

with open(sys.argv[1]) as f:
    d = f.read()
    regions = []
    shapes = []
    group = 0
    shape_ones = []

    sections = d.split("\n\n")
    for s in sections:
        shape_masks = None
        lines = s.split("\n")
        for line in lines:
            if not line:
                continue
            if line[-1] == ":":
                # Shape header
                shape_masks = []
                continue
            elif shape_masks is not None:
                v = 0
                shape_w = len(line)
                for i, c in enumerate(line):
                    if c == '#':
                        v |= 1 << i
                shape_masks.append(v)
            else:
                size, counts = line.split(": ")
                sx, sy = map(int, size.split("x"))
                counts = [int(v) for v in counts.split(" ")]
                regions.append(Region((sx, sy), counts))
        if shape_masks is not None:
            # Parse, add to shapes
            dims = (shape_w, len(shape_masks))
            n_ones = []
            n_zeroes = []
            for r in shape_masks:
                n_ones.append(r.bit_count())
                n_zeroes.append(shape_w - r.bit_count())
            shape_ones.append(sum(n_ones))
            shape = Shape(dims, group, tuple(shape_masks), tuple(n_ones), tuple(n_zeroes))
            group += 1

            xshapes = transform_shape(shape)
            shapes.extend(xshapes)

def draw_grid(rows, ncols = 1):
    # Make sure we draw _something_
    ncols = max(ncols, max(map(lambda v: v.bit_length(), rows)))
    for row in rows:
        s = ""
        for i in range(ncols):
            if row & (1 << i):
                s += "#"
            else:
                s += "."
        print(s)

# Row 0, bit 0, is top-left
# =========================

def still_possible(grid, counts, w):
    total_grid_cells = w * len(grid)
    total_zeroes_left = total_grid_cells - sum(r.bit_count() for r in grid)
    total_shape_ones = sum(
        shape_ones[i] * counts[i] for i in range(len(counts))
    )

    return total_shape_ones <= total_zeroes_left

# First, drop all the regions which trivially _won't_ fit
kept_regions = []
dropped = 0
for n, r in enumerate(regions):
    grid = [0] * r.dims[1]
    if still_possible(grid, r.counts, r.dims[0]):
        # We have to test it
        kept_regions.append(r)
    else:
        dropped += 1

print(f"{dropped=}, kept={len(kept_regions)}")

def score(shape, grid, x, y, w, h, roi):
    if x > (w - shape.dims[0]):
        return 0
    if y > (h - shape.dims[1]):
        return 0

    zeroes_removed = 0
    for i, mask in enumerate(shape.masks):
        if grid[y + i] & (mask << x):
            # Collision
            return 0
        roi_zeroes = roi[y + i] & (~grid[y + i])
        newly_set = (mask << x) & roi_zeroes
        zeroes_removed += newly_set.bit_count()
    return (zeroes_removed * 2) + 1


def place(shape, grid, x, y, roi):
    for i, mask in enumerate(shape.masks):
        grid[y + i] |= mask << x
        # XXX: Hard-coded shape width of 3...
        roi[y + i] |= (0x7 << x)

# Recursively place shapes around the edge of roi
def explore(grid, roi, counts, w, h):
    #print(f"{counts=}")
    if not still_possible(grid, counts, w):
        return False

    if counts == [0] * len(counts):
        draw_grid(grid, w)
        return True

    max_x = min(w, max(
        r.bit_length() for r in roi
    ) + 1)
    max_y = min(h, max(
        i if r > 0 else 0 for i, r in enumerate(roi)
    ) + 1)

    for y in range(max_y):
        for x in range(max_x):
            for i, shape in enumerate(shapes):
                if counts[shape.group] == 0:
                    # Quota met - don't place
                    continue

                s = score(shape, grid, x, y, w, h, roi)
                if s > 0:
                    new_grid, new_roi = grid.copy(), roi.copy()
                    place(shape, new_grid, x, y, new_roi)
                    placed = True
                    new_counts = counts.copy()
                    new_counts[shape.group] -= 1
                    if explore(new_grid, new_roi, new_counts, w, h):
                        return True
    return False

p1 = 0
# Now explore the ones which are left
for n, r in enumerate(kept_regions):
    print(n, r)

    w, h = r.dims

    grid = [0] * h

    # Initial ROI tries to fill the corner
    #  ###
    #  #..
    #  #..
    roi = [0] * h
    roi[0] = 0x7
    roi[1] = 0x1
    roi[2] = 0x1

    if explore(grid, roi, r.counts, w, h):
        p1 += 1

print(p1)
