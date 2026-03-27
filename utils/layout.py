import matplotlib.pyplot as plt
import matplotlib.patches as patches
from utils.stowage import compute_cog

# Warna tiap golongan
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

def plot_layout(items, L, W):
    fig, ax = plt.subplots(figsize=(50, 14))

    # Background terang agar axis terlihat
    ax.set_facecolor("#f0f0f0")
    fig.patch.set_facecolor("#111111")  # tetap dark background luar

    # Outline kapal
    ax.add_patch(
        patches.Rectangle(
            (0, 0),
            L,
            W,
            fill=False,
            linewidth=4,
            edgecolor="black"
        )
    )

    # Kendaraan
    for v in items:
        x = v["pos"][0] + L/2
        y = v["pos"][1] + W/2
        color = COLOR_MAP.get(v["name"], "cyan")

        ax.add_patch(
            patches.Rectangle(
                (x - v["length"]/2, y - v["width"]/2),
                v["length"],
                v["width"],
                fill=True,
                alpha=0.5,
                edgecolor=color,
                facecolor=color,
                linewidth=3
            )
        )

        ax.text(
            x, y,
            v["name"],
            ha="center",
            fontsize=20,
            color="black",
            weight="bold"
        )

    # CoG
    cx, cy = compute_cog(items)
    cx_v = cx + L/2
    cy_v = cy + W/2

    ax.scatter(cx_v, cy_v, color="red", s=300)
    ax.text(cx_v, cy_v, "CoG",
            fontsize=22, color="red", weight="bold")

    # Axis style
    ax.set_xlim(0, L)
    ax.set_ylim(0, W)
    ax.set_aspect("equal")

    # Axis labels besar & putih
    ax.set_xlabel("X (meter)", fontsize=20, color="white", labelpad=15)
    ax.set_ylabel("Y (meter)", fontsize=20, color="white", labelpad=15)

    # Angka axis putih & besar
    ax.tick_params(axis="x", colors="white", labelsize=18)
    ax.tick_params(axis="y", colors="white", labelsize=18)

    # Agar axis label tidak ketutup background gelap
    for spine in ax.spines.values():
        spine.set_color("white")

    return fig
