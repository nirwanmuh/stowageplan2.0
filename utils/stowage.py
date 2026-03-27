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

def auto_arrange(items, L, W, target_x_visual, target_y_visual):

    # convert to center coordinate system
    target_x = target_x_visual - L/2
    target_y = target_y_visual - W/2

    # urutkan kendaraan terberat
    items_sorted = sorted(items, key=lambda x: -x["weight"])
    placed = []

    def fits_in_ship(x, y, w, l):
        return (
            x - l/2 >= -L/2 and
            x + l/2 <=  L/2 and
            y - w/2 >= -W/2 and
            y + w/2 <=  W/2
        )

    def is_free(x, y, w, l):
        rect = (x, y, w, l)
        for p in placed:
            rect2 = (p["pos"][0], p["pos"][1], p["width"], p["length"])
            if overlap(rect, rect2):
                return False
        return True

    def can_place(x, y, w, l):
        return fits_in_ship(x, y, w, l) and is_free(x, y, w, l)

    # kendaraan pertama → tepat di CoG
    first = items_sorted[0]
    first["pos"] = (target_x, target_y)
    placed.append(first)

    # kendaraan berikutnya → mencari posisi terdekat
    for v in items_sorted[1:]:
        best_pos = None
        best_dist = 999999

        # radius besar dulu (maks 1/4 panjang kapal)
        for r in np.linspace(0, min(L, W)/3, 80):
            for angle in np.linspace(0, 2*np.pi, 180):
                x = target_x + r*np.cos(angle)
                y = target_y + r*np.sin(angle)

                if can_place(x, y, v["width"], v["length"]):
                    d = abs(x-target_x) + abs(y-target_y)
                    if d < best_dist:
                        best_dist = d
                        best_pos = (x, y)

            if best_pos:
                break

        if best_pos:
            v["pos"] = best_pos
        else:
            # fallback → letakkan di tempat aman terdekat kiri-kanan
            for x in np.linspace(-L/2, L/2, 200):
                for y in np.linspace(-W/2, W/2, 80):
                    if can_place(x, y, v["width"], v["length"]):
                        v["pos"] = (x, y)
                        best_pos = True
                        break
                if best_pos:
                    break

            if not best_pos:
                v["pos"] = (0, 0)  # benar‑benar fallback terakhir

        placed.append(v)

    return placed
    
def compute_cog(items):
    if not items:
        return (0, 0)

    total_w = sum(v["weight"] for v in items)
    X = sum(v["pos"][0] * v["weight"] for v in items) / total_w
    Y = sum(v["pos"][1] * v["weight"] for v in items) / total_w
    return (X, Y)
