import numpy as np
import copy

# ======================================================
# RECTANGLE OVERLAP CHECK (BENAR - length & width tepat)
# ======================================================
def overlap(r1, r2):
    x1, y1, l1, w1 = r1
    x2, y2, l2, w2 = r2

    return not (
        x1 + l1/2 <= x2 - l2/2 or
        x1 - l1/2 >= x2 + l2/2 or
        y1 + w1/2 <= y2 - w2/2 or
        y1 - w1/2 >= y2 + w2/2
    )

# ======================================================
# CHECK INSIDE SHIP BOUNDARIES
# ======================================================
def inside(x, y, l, w, L, W):
    return (
        x - l/2 >= -L/2 and
        x + l/2 <=  L/2 and
        y - w/2 >= -W/2 and
        y + w/2 <=  W/2
    )

# ======================================================
# CHECK NO COLLISION FOR ALL PLACED RECTANGLES
# ======================================================
def no_collision(x, y, w, l, placed):
    rect = (x, y, l, w)
    for p in placed:
        px, py = p["pos"]
        r2 = (px, py, p["length"], p["width"])
        if overlap(rect, r2):
            return False
    return True

# ======================================================
# AUTO ARRANGE (COG-driven)
# ======================================================
def auto_arrange(items, L, W, cog_visual_x, cog_visual_y):

    try:
        target_x = cog_visual_x - L/2
        target_y = cog_visual_y - W/2

        items_sorted = sorted(items, key=lambda x: -x["weight"])
        placed = []

        # first vehicle → center of CoG ship
        first = items_sorted[0]
        first["pos"] = (target_x, target_y)
        placed.append(first)

        # next vehicles
        for v in items_sorted[1:]:

            best = None
            best_dist = 999999

            # search around COG
            for r in np.linspace(0, min(L, W)/3, 80):
                for ang in np.linspace(0, 2*np.pi, 180):
                    x = target_x + r*np.cos(ang)
                    y = target_y + r*np.sin(ang)

                    if inside(x, y, v["length"], v["width"], L, W) and \
                       no_collision(x, y, v["width"], v["length"], placed):

                        d = abs(x-target_x) + abs(y-target_y)
                        if d < best_dist:
                            best_dist = d
                            best = (x, y)

                if best:
                    break

            # fallback brute
            if not best:
                for x in np.linspace(-L/2, L/2, 160):
                    for y in np.linspace(-W/2, W/2, 80):
                        if inside(x, y, v["length"], v["width"], L, W) and \
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

    except:
        return items

# ======================================================
# COMPUTE COG
# ======================================================
def compute_cog(items):
    total = sum(v["weight"] for v in items)
    if total == 0:
        return (0, 0)
    X = sum(v["pos"][0] * v["weight"] for v in items) / total
    Y = sum(v["pos"][1] * v["weight"] for v in items) / total
    return (X, Y)

# ======================================================
# OPTIMIZER - SWAP WITH NO-OVERLAP ENFORCEMENT
# ======================================================
def optimize_positions(items, L, W, target_x, target_y, iterations=200):

    def score(arr):
        cx, cy = compute_cog(arr)
        return abs(cx - target_x) + abs(cy - target_y)

    try:
        best = copy.deepcopy(items)
        best_score = score(best)

        for _ in range(iterations):

            i, j = np.random.choice(len(items), 2, replace=False)
            trial = copy.deepcopy(best)

            pos_i = trial[i]["pos"]
            pos_j = trial[j]["pos"]

            trial[i]["pos"], trial[j]["pos"] = pos_j, pos_i

            # check boundaries
            if not inside(trial[i]["pos"][0], trial[i]["pos"][1],
                          trial[i]["length"], trial[i]["width"], L, W):
                continue

            if not inside(trial[j]["pos"][0], trial[j]["pos"][1],
                          trial[j]["length"], trial[j]["width"], L, W):
                continue

            # global overlap check
            ok = True
            for a in range(len(trial)):
                for b in range(a+1, len(trial)):
                    ra = trial[a]
                    rb = trial[b]
                    r1 = (ra["pos"][0], ra["pos"][1], ra["length"], ra["width"])
                    r2 = (rb["pos"][0], rb["pos"][1], rb["length"], rb["width"])
                    if overlap(r1, r2):
                        ok = False
                        break
                if not ok:
                    break

            if not ok:
                continue

            # accept if CoG improved
            s = score(trial)
            if s < best_score:
                best = trial
                best_score = s

        return best

    except:
        return items
``
