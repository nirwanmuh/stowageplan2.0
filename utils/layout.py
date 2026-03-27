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

    # Outline kapal
    ax.add_patch(
        patches.Rectangle((0,0), L, W, fill=False, linewidth=4, edgecolor="black")
    )

    # Garis CoG kapal
    ax.axvline(empty_cog_x, color="blue", linestyle="--", linewidth=3)
    ax.axhline(empty_cog_y, color="blue", linestyle="--", linewidth=3)

    # Kendaraan
    for v in items:
        x = v["pos"][0] + L/2
        y = v["pos"][1] + W/2
        c = COLOR_MAP.get(v["name"], "cyan")

        ax.add_patch(
            patches.Rectangle(
                (x - v["length"]/2, y - v["width"]/2),
                v["length"], v["width"],
                fill=True, alpha=0.5,
                edgecolor=c, facecolor=c, linewidth=3
            )
        )

        ax.text(
            x, y, v["name"],
            fontsize=20, ha="center", weight="bold", color="black"
        )

    # CoG kendaraan
    cx, cy = compute_cog(items)
    ax.scatter(cx + L/2, cy + W/2, s=300, color="red")
    ax.text(cx + L/2, cy + W/2, "CoG Kendaraan", fontsize=22, color="red", weight="bold")

    # Axis
    ax.set_xlim(0, L)
    ax.set_ylim(0, W)
    ax.set_aspect("equal")

    ax.set_xlabel("Sumbu X (meter)", fontsize=20, color="white")
    ax.set_ylabel("Sumbu Y (meter)", fontsize=20, color="white")

    ax.tick_params(axis="x", colors="white", labelsize=18)
    ax.tick_params(axis="y", colors="white", labelsize=18)

    for spine in ax.spines.values():
        spine.set_color("white")

    return fig
