import numpy as np
import copy

# ====================================================
# RECTANGLE OVERLAP CHECK
# ====================================================
def overlap(a, b):
    ax, ay, aw, al = a
    bx, by, bw, bl = b

    return not (
        ax + al/2 <= bx - bl/2 or
        ax - al/2 >= bx + bl/2 or
        ay + aw/2 <= by - bw/2 or
        ay - aw/2 >= by + bw/2
    )

# ====================================================
# FIT INSIDE SHIP
# ====================================================
def rect_inside_ship(x, y, w, l, L, W):
    return (
        x - l/2 >= -L/2 and
        x + l/2 <=  L/2 and
        y - w/2 >= -W/2 and
        y + w/2 <=  W/2
    )

# ====================================================
# NO COLLISION CHECK
# ====================================================
def no_collision(x, y, w, l, placed):
    rect = (x, y, w, l)
    for p in placed:
        pr = (p["pos"][0], p["pos"][1], p["width"], p["length"])
        if overlap(rect, pr):
            return False
    return True

# ====================================================
# AUTO ARRANGE (COG DRIVEN)
# ====================================================
def auto_arrange(items, L, W, target_visual_x, target_visual_y):

    target_x = target_visual_x - L/2
    target_y = target_visual_y - W/2

    items_sorted = sorted(items, key=lambda x: -x["weight"])
    placed = []

    # Kendaraan pertama → CoG kapal
    first = items_sorted[0]
    first["pos"] = (target_x, target_y)
    placed.append(first)

    # Kendaraan berikutnya
    for v in items_sorted[1:]:

        best = None
        best_dist = 999999

        for r in np.linspace(0, min(L, W)/3, 80):
            for angle in np.linspace(0, 2*np.pi, 180):

                x = target_x + r*np.cos(angle)
                y = target_y + r*np.sin(angle)

                if rect_inside_ship(x, y, v["width"], v["length"], L, W) and \
                   no_collision(x, y, v["width"], v["length"], placed):

                    d = abs(x-target_x) + abs(y-target_y)
                    if d < best_dist:
                        best_dist = d
                        best = (x, y)

            if best:
                break

        # fallback
        if not best:
            for x in np.linspace(-L/2, L/2, 150):
                for y in np.linspace(-W/2, W/2, 60):
                    if rect_inside_ship(x, y, v["width"], v["length"], L, W) and \
                       no_collision(x, y, v["width"], v["length"], placed):
                        best = (x, y)
                        break
                if best:
                    break

        if not best:
            best = (0, 0)

        v["pos"] = best
        placed.append(v)

    return placed

# ====================================================
# COG KENDARAAN
# ====================================================
def compute_cog(items):
    total_w = sum(v["weight"] for v in items)
    if total_w == 0:
        return (0, 0)
    X = sum(v["pos"][0] * v["weight"] for v in items) / total_w
    Y = sum(v["pos"][1] * v["weight"] for v in items) / total_w
    return (X, Y)

# ====================================================
# OPTIMIZATION (SWAP POSITIONS)
# ====================================================
def optimize_positions(items, L, W, target_x, target_y, iterations=300):

    def score(arr):
        cx, cy = compute_cog(arr)
        return abs(cx - target_x) + abs(cy - target_y)

    best = copy.deepcopy(items)
    best_score = score(best)

    for _ in range(iterations):

        i, j = np.random.choice(len(items), 2, replace=False)
        trial = copy.deepcopy(best)

        trial[i]["pos"], trial[j]["pos"] = trial[j]["pos"], trial[i]["pos"]

        s = score(trial)
        if s < best_score:
            best = trial
            best_score = s

    return best
