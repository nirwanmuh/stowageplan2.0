import numpy as np

def overlap(a, b):
    ax, ay, aw, al = a
    bx, by, bw, bl = b

    return not (
        ax + al/2 <= bx - bl/2 or
        ax - al/2 >= bx + bl/2 or
        ay + aw/2 <= by - bw/2 or
        ay - aw/2 >= by + bw/2
    )

def auto_arrange(items, L, W, target_x, target_y):
    # Sort descending by weight
    items_sorted = sorted(items, key=lambda x: -x["weight"])

    placed = []

    # Helper to check placement validity
    def can_place(x, y, w, l):
        # check bounds
        if not (-L/2 <= x <= L/2 and -W/2 <= y <= W/2):
            return False

        rect = (x, y, w, l)
        for p in placed:
            rect2 = (p["pos"][0], p["pos"][1], p["width"], p["length"])
            if overlap(rect, rect2):
                return False
        return True

    # First vehicle is placed exactly at CoG target
    for idx, v in enumerate(items_sorted):
        if idx == 0:
            v["pos"] = (target_x, target_y)
            placed.append(v)
            continue

        # Generate candidate locations around CoG
        search_radius = 0.5
        best_pos = None
        best_dist = 999999

        for r in np.linspace(0, 10, 40):  # expand outward
            for angle in np.linspace(0, 2*np.pi, 36):
                x = target_x + r*np.cos(angle)
                y = target_y + r*np.sin(angle)

                if can_place(x, y, v["width"], v["length"]):
                    # choose position closest to target CoG
                    d = np.sqrt((x-target_x)**2 + (y-target_y)**2)
                    if d < best_dist:
                        best_dist = d
                        best_pos = (x, y)

            if best_pos:
                v["pos"] = best_pos
                placed.append(v)
                break

        if best_pos is None:
            # fallback
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
