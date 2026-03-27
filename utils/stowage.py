import numpy as np

# ----- OVERLAP CHECK -----
def overlap(a, b):
    ax, ay, aw, al = a
    bx, by, bw, bl = b

    return not (
        ax + al/2 <= bx - bl/2 or
        ax - al/2 >= bx + bl/2 or
        ay + aw/2 <= by - bw/2 or
        ay - aw/2 >= by + bw/2
    )

# ----- AUTO ARRANGE -----
def auto_arrange(items, L, W):
    if not isinstance(items, list):
        return []

    items_sorted = sorted(items, key=lambda x: -x["weight"])

    placed = []
    radius_step = min(L, W) * 0.12
    angle_step = np.radians(25)

    r = 0
    theta = 0

    for v in items_sorted:
        found = False
        attempt = 0

        while not found and attempt < 4000:
            x = r * np.cos(theta)
            y = r * np.sin(theta)

            rect = (x, y, v["width"], v["length"])
            ok = True

            # cek overlap
            for p in placed:
                rect2 = (p["pos"][0], p["pos"][1], p["width"], p["length"])
                if overlap(rect, rect2):
                    ok = False
                    break

            # cek batas
            if not (-L/2 <= x <= L/2 and -W/2 <= y <= W/2):
                ok = False

            if ok:
                v["pos"] = (x, y)
                placed.append(v)
                found = True
                break

            theta += angle_step
            if theta >= 2 * np.pi:
                theta = 0
                r += radius_step

            attempt += 1

        if not found:
            v["pos"] = (0, 0)
            placed.append(v)

    return placed


def compute_cog(items):
    if not items:
        return (0, 0)

    total_w = sum(v["weight"] for v in items)
    X = sum(v["pos"][0] * v["weight"] for v in items) / total_w
    Y = sum(v["pos"][1] * v["weight"] for v in items) / total_w
    return (X, Y)
