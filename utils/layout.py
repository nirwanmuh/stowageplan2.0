import matplotlib.pyplot as plt
import matplotlib.patches as patches
from utils.stowage import compute_cog

def plot_layout(items, L, W):
    # FIGURE SUPER BESAR
    fig, ax = plt.subplots(figsize=(32, 12))  # full screen feel

    # Outline kapal
    ax.add_patch(
        patches.Rectangle(
            (-L/2, -W/2),
            L,
            W,
            fill=False,
            linewidth=3,
            edgecolor="black"
        )
    )

    # Kendaraan
    for v in items:
        x, y = v["pos"]
        ax.add_patch(
            patches.Rectangle(
                (x - v["length"]/2, y - v["width"]/2),
                v["length"],
                v["width"],
                fill=False,
                edgecolor="blue",
                linewidth=2
            )
        )
        ax.text(x, y, v.get("name", "kendaraan"), ha="center", fontsize=12)

    # Center of Gravity
    cx, cy = compute_cog(items)
    ax.scatter(cx, cy, color="red", s=120)
    ax.text(cx, cy, "CoG", fontsize=14, color="red")

    ax.set_xlim(-L/2, L/2)
    ax.set_ylim(-W/2, W/2)
    ax.set_aspect("equal")

    return fig
