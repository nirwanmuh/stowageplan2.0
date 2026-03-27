import matplotlib.pyplot as plt
import matplotlib.patches as patches
from utils.stowage import compute_cog, get_bbox

COLOR = {
    "Golongan I": "cyan",
    "Golongan II": "yellow",
    "Golongan III": "orange",
    "Golongan IVA": "green",
    "Golongan IVB": "lime",
    "Golongan VA": "purple",
    "Golongan VB": "violet",
    "Golongan VIB": "magenta",
    "Golongan VII": "red",
    "Golongan VIII": "deeppink",
    "Golongan IX": "gold"
}

def plot_layout(items, ship_L, ship_W, cog_x, cog_y):

    fig, ax = plt.subplots(figsize=(50,14))
    ax.set_facecolor("#f0f0f0")
    fig.patch.set_facecolor("#111111")

    # outline kapal
    ax.add_patch(
        patches.Rectangle((0,0), ship_L, ship_W, fill=False, linewidth=4, edgecolor="black")
    )

    # garis CoG
    ax.axvline(cog_x, color="blue", linestyle="--", linewidth=3)
    ax.axhline(cog_y, color="blue", linestyle="--", linewidth=3)

    # kendaraan
    for v in items:
        cx, cy = v["pos"]
        vx = cx + ship_L/2
        vy = cy + ship_W/2

        xmin, xmax, ymin, ymax = get_bbox(cx, cy, v["length"], v["width"])
        xmin += ship_L/2
        xmax += ship_L/2
        ymin += ship_W/2
        ymax += ship_W/2

        c = COLOR.get(v["name"], "cyan")

        ax.add_patch(
            patches.Rectangle(
                (xmin, ymin),
                v["length"], v["width"],
                fill=True, edgecolor=c, facecolor=c, alpha=0.5, linewidth=3
            )
        )
        ax.text((xmin+xmax)/2, (ymin+ymax)/2,
                v["name"], fontsize=20, ha="center", weight="bold")

    # CoG kendaraan
    cx, cy = compute_cog(items)
    ax.scatter(cx+ship_L/2, cy+ship_W/2, color="red", s=300)
    ax.text(cx+ship_L/2, cy+ship_W/2, "CoG", fontsize=22, color="red")

    ax.set_xlim(0, ship_L)
    ax.set_ylim(0, ship_W)
    ax.set_aspect("equal")

    return fig
