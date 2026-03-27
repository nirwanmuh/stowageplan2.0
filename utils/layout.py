import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from utils.stowage import get_bbox, compute_cog_pos

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

def plot_layout(items, Ls, Ws, cog_x, cog_y):

    fig, ax = plt.subplots(figsize=(50,14))
    ax.set_facecolor("#f0f0f0")
    fig.patch.set_facecolor("#111111")

    # outline
    ax.add_patch(patches.Rectangle((0,0), Ls, Ws,
                                   fill=False, edgecolor="black", linewidth=4))

    # CoG lines
    ax.axvline(cog_x, color="blue", linestyle="--", linewidth=3)
    ax.axhline(cog_y, color="blue", linestyle="--", linewidth=3)

    # Prepare CoG computation
    positions = np.array([v["pos"] for v in items])
    weights   = np.array([v["weight"] for v in items])

    # Draw vehicles
    for v in items:
        cx, cy = v["pos"]
        L, W = v["length"], v["width"]

        xmin, xmax, ymin, ymax = get_bbox(cx, cy, L, W)

        xmin += Ls/2
        xmax += Ls/2
        ymin += Ws/2
        ymax += Ws/2

        c = COLOR.get(v["name"], "cyan")

        ax.add_patch(
            patches.Rectangle(
                (xmin, ymin), L, W,
                fill=True, facecolor=c, edgecolor=c, alpha=0.5, linewidth=3
            )
        )

        ax.text(
            (xmin+xmax)/2,
            (ymin+ymax)/2,
            v["name"],
            fontsize=16,
            ha="center", va="center",
            weight="bold"
        )

    # CoG kendaraan
    cx2, cy2 = compute_cog_pos(positions, weights)
    ax.scatter(cx2 + Ls/2, cy2 + Ws/2, s=300, color="red")

    ax.set_xlim(0, Ls)
    ax.set_ylim(0, Ws)
    ax.set_aspect("equal")

    return fig
