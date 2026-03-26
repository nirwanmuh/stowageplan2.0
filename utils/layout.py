import matplotlib.pyplot as plt
import matplotlib.patches as patches
from utils.stowage import compute_cog

def plot_layout(items, L, W):
    fig, ax = plt.subplots(figsize=(10, 5))

    # kapal
    ax.add_patch(
        patches.Rectangle((-L/2, -W/2), L, W, fill=False, linewidth=2)
    )

    # kendaraan
    for v in items:
        x, y = v["pos"]
        ax.add_patch(
            patches.Rectangle(
                (x - v["length"] / 2, y - v["width"] / 2),
                v["length"], v["width"],
                fill=False, edgecolor="blue"
            )
        )
        ax.text(x, y, v.get("name", "Vehicle"), ha="center", fontsize=7)

    # titik CoG
    cx, cy = compute_cog(items)
    ax.scatter(cx, cy, color="red")
    ax.text(cx, cy, "CoG", color="red")

    ax.set_xlim(-L/2, L/2)
    ax.set_ylim(-W/2, W/2)
    ax.set_aspect("equal")

    return fig
