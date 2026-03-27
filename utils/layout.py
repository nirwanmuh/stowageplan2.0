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

    # Outline kapal (dengan sistem koordinat 0,0 pojok kiri bawah)
    ax.add_patch(
        patches.Rectangle(
            (0, 0),
            L,
            W,
            fill=False,
            linewidth=4,
            edgecolor="white"
        )
    )

    # Gambar kendaraan
    for v in items:
        # offset agar posisi jadi sistem pojok kiri bawah
        x = v["pos"][0] + L/2
        y = v["pos"][1] + W/2

        color = COLOR_MAP.get(v["name"], "cyan")

        ax.add_patch(
            patches.Rectangle(
                (x - v["length"]/2, y - v["width"]/2),
                v["length"],
                v["width"],
                fill=True,
                alpha=0.4,
                edgecolor=color,
                facecolor=color,
                linewidth=3
            )
        )

        ax.text(
            x,
            y,
            v["name"],
            ha="center",
            fontsize=18,
            color="white",
            weight="bold"
        )

    # Hitung CoG
    cx, cy = compute_cog(items)
    cx_visual = cx + L/2
    cy_visual = cy + W/2

    ax.scatter(cx_visual, cy_visual, color="red", s=300)
    ax.text(cx_visual, cy_visual, "CoG", color="red", fontsize=20, weight="bold")

    # Atur tampilan
    ax.set_xlim(0, L)
    ax.set_ylim(0, W)
    ax.set_aspect("equal")

    # Warna background
    ax.set_facecolor("#111111")
    fig.patch.set_facecolor("#111111")

    return fig
