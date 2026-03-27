import matplotlib.pyplot as plt
import matplotlib.patches as patches
from utils.stowage import compute_cog

COLOR_MAP = {
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

def plot_layout(items, L, W, empty_cog_x, empty_cog_y):

    fig, ax = plt.subplots(figsize=(50, 14))
    ax.set_facecolor("#f0f0f0")
    fig.patch.set_facecolor("#111111")

    # outline kapal
    ax.add_patch(
        patches.Rectangle((0,0), L, W, fill=False, linewidth=4, edgecolor="black")
    )

    # garis CoG
    ax.axvline(empty_cog_x, color="blue", linestyle="--", linewidth=3)
    ax.axhline(empty_cog_y, color="blue", linestyle="--", linewidth=3)

    for v in items:
        # center → visual
        vx = v["pos"][0] + L/2
        vy = v["pos"][1] + W/2

        # CLAMP rectangle agar tidak terpotong
        vx = max(v["length"]/2, min(L - v["length"]/2, vx))
        vy = max(v["width"]/2,  min(W - v["width"]/2,  vy))

        c = COLOR_MAP.get(v["name"], "cyan")

        ax.add_patch(
            patches.Rectangle(
                (vx - v["length"]/2, vy - v["width"]/2),
                v["length"], v["width"],
                fill=True, alpha=0.5,
                edgecolor=c, facecolor=c, linewidth=3
            )
        )

        ax.text(vx, vy, v["name"],
                fontsize=20, ha="center", color="black", weight="bold")

    # COG kendaraan
    cx, cy = compute_cog(items)
    cx_v = cx + L/2
    cy_v = cy + W/2

    ax.scatter(cx_v, cy_v, s=300, color="red")
    ax.text(cx_v, cy_v, "CoG", fontsize=22, color="red", weight="bold")

    # axis
    ax.set_xlim(0, L)
    ax.set_ylim(0, W)
    ax.set_aspect("equal")

    ax.tick_params(axis="x", colors="white", labelsize=18)
    ax.tick_params(axis="y", colors="white", labelsize=18)

    for spine in ax.spines.values():
        spine.set_color("white")

    return fig
