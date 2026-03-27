import numpy as np
import copy

# ==========================
# RECTANGLE OVERLAP CHECK
# ==========================
def rectangles_overlap(x1, y1, L1, W1, x2, y2, L2, W2):
    return not (
        x1 + L1/2 <= x2 - L2/2 or
        x1 - L1/2 >= x2 + L2/2 or
        y1 + W1/2 <= y2 - W2/2 or
        y1 - W1/2 >= y2 + W2/2
    )

# ==========================
# CHECK ALL COLLISIONS
# ==========================
def global_no_overlap(items):
    n = len(items)
    for i in range(n):
        for j in range(i+1, n):
            a = items[i]
            b = items[j]
            if rectangles_overlap(
                a["pos"][0], a["pos"][1], a["length"], a["width"],
                b["pos"][0], b["pos"][1], b["length"], b["width"]
            ):
                return False
    return True

# ==========================
# CHECK INSIDE SHIP
# ==========================
def inside(x, y, L, W, Ls, Ws):
    return (
        x - L/2 >= -Ls/2 and
        x + L/2 <=  Ls/2 and
        y - W/2 >= -Ws/2 and
        y + W/2 <=  Ws/2
    )

# ==========================
# AUTO ARRANGE (COG DRIVEN)
# ==========================
def auto_arrange(items, Ls, Ws, cog_x_visual, cog_y_visual):

    target_x = cog_x_visual - Ls/2
    target_y = cog_y_visual - Ws/2

    sorted_items = sorted(items, key=lambda v: -v["weight"])
    placed = []

    # kendaraan pertama di CoG
    first = sorted_items[0]
    first["pos"] = (target_x, target_y)
    placed.append(first)

    # kendaraan lain
    for v in sorted_items[1:]:

        best = None
        best_dist = 1e18

        for r in np.linspace(0, min(Ls, Ws)/2, 200):
            for ang in np.linspace(0, np.pi*2, 200):

                x = target_x + r*np.cos(ang)
                y = target_y + r*np.sin(ang)

                # inside check
                if not inside(x, y, v["length"], v["width"], Ls, Ws):
                    continue

                # collision check
                ok = True
                for p in placed:
                    if rectangles_overlap(
                        x, y, v["length"], v["width"],
                        p["pos"][0], p["pos"][1], p["length"], p["width"]
                    ):
                        ok = False
                        break
                if not ok:
                    continue

                # choose nearest to CoG
                d = abs(x - target_x) + abs(y - target_y)
                if d < best_dist:
                    best_dist = d
                    best = (x, y)

            if best:
                break

        if not best:
            # emergency fallback — place near center line
            for x in np.linspace(-Ls/2, Ls/2, 200):
                for y in np.linspace(-Ws/2, Ws/2, 200):

                    if not inside(x, y, v["length"], v["width"], Ls, Ws):
                        continue

                    ok = True
                    for p in placed:
                        if rectangles_overlap(
                            x, y, v["length"], v["width"],
                            p["pos"][0], p["pos"][1], p["length"], p["width"]
                        ):
                            ok = False
                            break
                    if ok:
                        best = (x, y)
                        break
                if best:
                    break

        if not best:
            best = (0,0)

        v["pos"] = best
        placed.append(v)

    return placed

# ==========================
# COG PERHITUNGAN
# ==========================
def compute_cog(items):
    total = sum(v["weight"] for v in items)
    if total == 0:
        return (0,0)
    X = sum(v["pos"][0]*v["weight"] for v in items)/total
    Y = sum(v["pos"][1]*v["weight"] for v in items)/total
    return (X,Y)

# ==========================
# OPTIMIZER (NO OVERLAP GUARANTEED)
# ==========================
def optimize_positions(items, Ls, Ws, tx, ty, iterations=200):

    def score(arr):
        cx, cy = compute_cog(arr)
        return abs(cx - tx) + abs(cy - ty)

    best = copy.deepcopy(items)
    best_score = score(best)

    for _ in range(iterations):

        import random
        i, j = random.sample(range(len(items)), 2)

        trial = copy.deepcopy(best)

        # swap
        trial[i]["pos"], trial[j]["pos"] = trial[j]["pos"], trial[i]["pos"]

        # validate all
        if not global_no_overlap(trial):
            continue

        s = score(trial)
        if s < best_score:
            best = trial
            best_score = s

    return best
``
