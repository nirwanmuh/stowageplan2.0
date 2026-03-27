import matplotlib.pyplot as plt
import matplotlib.patches as patches
from utils.stowage import get_bbox, compute_cog

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

    fig, ax = plt.subplots(figsize=(50, 14))
    ax.set_facecolor("#f0f0f0")
    fig.patch.set_facecolor("#111111")

    # Ship outline
    ax.add_patch(patches.Rectangle((0,0), Ls, Ws,
                                   fill=False, linewidth=4, edgecolor='black'))

    ax.axvline(cog_x, color="blue", linestyle="--", linewidth=3)
    ax.axhline(cog_y, color="blue", linestyle="--", linewidth=3)

    for v in items:
        cx, cy = v["pos"]
        bbox = get_bbox(cx, cy, v["length"], v["width"])

        xmin = bbox[0] + Ls/2
        xmax = bbox[1] + Ls/2
        ymin = bbox[2] + Ws/2
        ymax = bbox[3] + Ws/2

        c = COLOR.get(v["name"], "cyan")

        ax.add_patch(
            patches.Rectangle(
                (xmin, ymin),
                v["length"], v["width"],
                fill=True, edgecolor=c, facecolor=c, alpha=0.5, linewidth=3
            )
        )

        ax.text((xmin+xmax)/2, (ymin+ymax)/2,
                v["name"], color="black", fontsize=18, weight="bold",
                ha="center", va="center")

    # Final CoG
    cx, cy = compute_cog(items)
    ax.scatter(cx + Ls/2, cy + Ws/2, color="red", s=300)
    ax.text(cx + Ls/2, cy + Ws/2, "CoG", fontsize=22, color="red")

    ax.set_xlim(0, Ls)
    ax.set_ylim(0, Ws)
    ax.set_aspect("equal")

    return fig
