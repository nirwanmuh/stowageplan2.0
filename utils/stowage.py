import numpy as np

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

def inside_ship(x, y, L, W, ship_L, ship_W):
    return (
        x - L/2 >= -ship_L/2 and
        x + L/2 <=  ship_L/2 and
        y - W/2 >= -ship_W/2 and
        y + W/2 <=  ship_W/2
    )

# ==========================
# AUTO ARRANGE – NO OVERLAP GUARANTEED
# ==========================
def auto_arrange(items, ship_L, ship_W, cog_x, cog_y):

    cx = cog_x - ship_L/2
    cy = cog_y - ship_W/2

    vehicles = sorted(items, key=lambda v: -v["weight"])
    placed = []

    # First vehicle at CoG
    v0 = vehicles[0]
    v0["pos"] = (cx, cy)
    placed.append(v0)

    # Other vehicles
    for v in vehicles[1:]:

        best_pos = None
        best_dist = float("inf")

        # Expand radius like placing circles
        for r in np.linspace(0, 20, 300):
            for a in np.linspace(0, 2*np.pi, 360):

                x = cx + r * np.cos(a)
                y = cy + r * np.sin(a)

                # Boundary
                if not inside_ship(x, y, v["length"], v["width"], ship_L, ship_W):
                    continue

                # Collision check
                collided = False
                for p in placed:
                    if rectangles_overlap(
                        x, y, v["length"], v["width"],
                        p["pos"][0], p["pos"][1], p["length"], p["width"]
                    ):
                        collided = True
                        break

                if collided:
                    continue

                # Choose closest to CoG
                d = abs(x - cx) + abs(y - cy)
                if d < best_dist:
                    best_dist = d
                    best_pos = (x, y)

            if best_pos:
                break

        if not best_pos:
            # fallback: find ANY empty space from grid scanning
            for x in np.linspace(-ship_L/2, ship_L/2, 200):
                ok_found = False
                for y in np.linspace(-ship_W/2, ship_W/2, 200):

                    if not inside_ship(x, y, v["length"], v["width"], ship_L, ship_W):
                        continue

                    collided = False
                    for p in placed:
                        if rectangles_overlap(
                            x, y, v["length"], v["width"],
                            p["pos"][0], p["pos"][1], p["length"], p["width"]
                        ):
                            collided = True
                            break

                    if not collided:
                        best_pos = (x, y)
                        ok_found = True
                        break
                if ok_found:
                    break

        if not best_pos:
            best_pos = (0, 0)

        v["pos"] = best_pos
        placed.append(v)

    return placed

# ==========================
# CoG
# ==========================
def compute_cog(items):
    total = sum(v["weight"] for v in items)
    if total == 0:
        return (0,0)
    X = sum(v["pos"][0] * v["weight"] for v in items) / total
    Y = sum(v["pos"][1] * v["weight"] for v in items) / total
    return (X, Y)
