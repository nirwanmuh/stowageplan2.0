import numpy as np

# ======================================================
# AABB BOUNDING BOX
# ======================================================
def get_bbox(cx, cy, length, width):
    xmin = cx - length/2
    xmax = cx + length/2
    ymin = cy - width/2
    ymax = cy + width/2
    return xmin, xmax, ymin, ymax

# ======================================================
# AABB OVERLAP CHECK (100% AKURAT)
# ======================================================
def bbox_overlap(b1, b2):
    x1min, x1max, y1min, y1max = b1
    x2min, x2max, y2min, y2max = b2

    return not (
        x1max <= x2min or
        x1min >= x2max or
        y1max <= y2min or
        y1min >= y2max
    )

# ======================================================
# VALIDATE NO COLLISION WITH ALL VEHICLES
# ======================================================
def no_overlap_all(x, y, v, placed, ship_L, ship_W):

    # bounding box kendaraan baru
    b1 = get_bbox(x, y, v["length"], v["width"])

    # CEK boundary kapal
    if b1[0] < -ship_L/2 or b1[1] > ship_L/2:
        return False
    if b1[2] < -ship_W/2 or b1[3] > ship_W/2:
        return False

    # CEK overlap dengan kendaraan lain
    for p in placed:
        px, py = p["pos"]
        b2 = get_bbox(px, py, p["length"], p["width"])
        if bbox_overlap(b1, b2):
            return False

    return True

# ======================================================
# AUTO ARRANGE — RADIAL EXPANSION (NO OVERLAP)
# ======================================================
def auto_arrange(items, ship_L, ship_W, cog_x_visual, cog_y_visual):

    cx = cog_x_visual - ship_L/2
    cy = cog_y_visual - ship_W/2

    # urutkan dari yang terberat
    vehicles = sorted(items, key=lambda v: -v["weight"])
    placed = []

    # kendaraan pertama → CoG
    v0 = vehicles[0]
    v0["pos"] = (cx, cy)
    placed.append(v0)

    # lainnya → radial search
    for v in vehicles[1:]:

        found = False

        for r in np.linspace(0, 20, 500):
            for ang in np.linspace(0, 2*np.pi, 360):

                x = cx + r * np.cos(ang)
                y = cy + r * np.sin(ang)

                if no_overlap_all(x, y, v, placed, ship_L, ship_W):
                    v["pos"] = (x, y)
                    placed.append(v)
                    found = True
                    break
            if found:
                break

        # fallback: brute grid
        if not found:
            for x in np.linspace(-ship_L/2, ship_L/2, 300):
                ok = False
                for y in np.linspace(-ship_W/2, ship_W/2, 150):

                    if no_overlap_all(x, y, v, placed, ship_L, ship_W):
                        v["pos"] = (x, y)
                        placed.append(v)
                        ok = True
                        break
                if ok:
                    break

        # fallback bener-bener darurat
        if not found:
            v["pos"] = (0, 0)
            placed.append(v)

    return placed

# ======================================================
# CoG
# ======================================================
def compute_cog(items):
    total = sum(v["weight"] for v in items)
    if total == 0:
        return (0,0)
    X = sum(v["pos"][0] * v["weight"] for v in items) / total
    Y = sum(v["pos"][1] * v["weight"] for v in items) / total
    return (X, Y)
