import random
import matplotlib.pyplot as plt

# =========================
# CONFIGURATION
# =========================

CANVAS_W = 100
CANVAS_H = 70

SHAPE_COUNT = 220

MIN_SIZE = 3
MAX_SIZE = 18

MAX_ATTEMPTS = 500

BACKGROUND = "#080B12"
LINE_COLOR = "#E8E8E8"
LINE_WIDTH = 0.5


# =========================
# SHAPE GENERATOR
# =========================

def create_shape():
    shape_type = random.choice(["L", "U", "C"])

    w = random.randint(MIN_SIZE, MAX_SIZE)
    h = random.randint(MIN_SIZE, MAX_SIZE)

    if shape_type == "L":

        points = [
            (0, 0),
            (w, 0),
            (w, h)
        ]

    elif shape_type == "U":

        left_height = random.randint(MIN_SIZE, MAX_SIZE)
        right_height = random.randint(MIN_SIZE, MAX_SIZE)

        if random.random() > 0.35:
            right_height = left_height

        points = [
            (0, left_height),
            (0, 0),
            (w, 0),
            (w, right_height)
        ]

    else:  # C shape

        top_width = random.randint(MIN_SIZE, MAX_SIZE)
        bottom_width = random.randint(MIN_SIZE, MAX_SIZE)

        points = [
            (top_width, 0),
            (0, 0),
            (0, h),
            (bottom_width, h)
        ]

    # Random rotation
    rotation = random.choice([0, 90, 180, 270])

    rotated = []

    for x, y in points:

        if rotation == 0:
            nx, ny = x, y

        elif rotation == 90:
            nx, ny = -y, x

        elif rotation == 180:
            nx, ny = -x, -y

        else:
            nx, ny = y, -x

        rotated.append((nx, ny))

    # Normalize coordinates
    min_x = min(x for x, y in rotated)
    min_y = min(y for x, y in rotated)

    rotated = [
        (x - min_x, y - min_y)
        for x, y in rotated
    ]

    return rotated


# =========================
# INTERSECTION CHECK
# =========================

def intersects(a, b, c, d):
    ax, ay = a
    bx, by = b
    cx, cy = c
    dx, dy = d

    # Both horizontal
    if ay == by and cy == dy:

        if ay != cy:
            return False

        return max(min(ax, bx), min(cx, dx)) <= \
            min(max(ax, bx), max(cx, dx))

    # Both vertical
    if ax == bx and cx == dx:

        if ax != cx:
            return False

        return max(min(ay, by), min(cy, dy)) <= \
            min(max(ay, by), max(cy, dy))

    # Horizontal and vertical
    if ay == by:
        return (
                min(ax, bx) <= cx <= max(ax, bx)
                and min(cy, dy) <= ay <= max(cy, dy)
        )

    return (
            min(cx, dx) <= ax <= max(cx, dx)
            and min(ay, by) <= cy <= max(ay, by)
    )


# =========================
# VALIDATION
# =========================

def is_valid(new_segments, existing_segments):
    for a, b in new_segments:

        for c, d in existing_segments:

            if intersects(a, b, c, d):
                return False

    return True


# =========================
# PATTERN GENERATION
# =========================

all_segments = []
accepted_shapes = []

cell_w = CANVAS_W / 5
cell_h = CANVAS_H / 4

for _ in range(SHAPE_COUNT):

    for attempt in range(MAX_ATTEMPTS):

        points = create_shape()

        # Distribute placement across regions
        region_x = random.randint(0, 4)
        region_y = random.randint(0, 3)

        offset_x = int(
            region_x * cell_w + random.uniform(0, cell_w)
        )

        offset_y = int(
            region_y * cell_h + random.uniform(0, cell_h)
        )

        points = [
            (x + offset_x, y + offset_y)
            for x, y in points
        ]

        # Canvas boundary check
        if any(
                x < 2 or y < 2 or
                x > CANVAS_W - 2 or y > CANVAS_H - 2
                for x, y in points
        ):
            continue

        # Create segments
        new_segments = list(
            zip(points[:-1], points[1:])
        )

        # Validate
        if is_valid(new_segments, all_segments):
            all_segments.extend(new_segments)
            accepted_shapes.append(points)

            break

# =========================
# DRAWING
# =========================

fig, ax = plt.subplots(figsize=(16, 11))

fig.patch.set_facecolor(BACKGROUND)
ax.set_facecolor(BACKGROUND)

for shape in accepted_shapes:

    for a, b in zip(shape[:-1], shape[1:]):
        ax.plot(
            [a[0], b[0]],
            [a[1], b[1]],
            color=LINE_COLOR,
            linewidth=LINE_WIDTH,
            solid_capstyle="round"
        )

ax.set_xlim(0, CANVAS_W)
ax.set_ylim(0, CANVAS_H)

ax.set_aspect("equal")
ax.axis("off")

plt.tight_layout()
plt.show()

print("Generated shapes:", len(accepted_shapes))
print("Total line segments:", len(all_segments))
