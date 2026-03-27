import matplotlib.pyplot as plt
import matplotlib.patches as patches
from utils.stowage import compute_cog

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

def plot_layout(items, L, W, cog_x, cog_y):

    fig, ax = plt.subplots(figsize=(50, 14))
    ax.set_facecolor("#f0f0f0")
    fig.patch.set_facecolor("#111111")

    # outline kapal
    ax.add_patch(
        patches.Rectangle((0,0), L, W, fill=False, linewidth=4, edgecolor="black")
    )

    # garis CoG kapal
    ax.axvline(cog_x, color="blue", linestyle="--", linewidth=3)
    ax.axhline(cog_y, color="blue", linestyle="--", linewidth=3)

    for v in items:
        vx = v["pos"][0] + L/2
        vy = v["pos"][1] + W/2

        # clamp supaya tidak kepotong
        vx = max(v["length"]/2, min(L - v["length"]/2, vx))
        vy = max(v["width"]/2,  min(W - v["width"]/2,  vy))

        c = COLOR.get(v["name"], "cyan")

        ax.add_patch(
            patches.Rectangle(
                (vx - v["length"]/2, vy - v["width"]/2),
                v["length"], v["width"],
                fill=True, alpha=0.5,
                edgecolor=c, facecolor=c, linewidth=3
            )
        )

        ax.text(vx, vy, v["name"],
                fontsize=20, ha="center", weight="bold", color="black")

    # CoG kendaraan
    cx, cy = compute_cog(items)
    ax.scatter(cx + L/2, cy + W/2, s=300, color="red")
    ax.text(cx + L/2, cy + W/2, "CoG", fontsize=22, weight="bold", color="red")

    ax.set_xlim(0, L)
    ax.set_ylim(0, W)
    ax.set_aspect("equal")

    ax.tick_params(axis="x", colors="white", labelsize=18)
    ax.tick_params(axis="y", colors="white", labelsize=18)

    for spine in ax.spines.values():
        spine.set_color("white")

    return fig
