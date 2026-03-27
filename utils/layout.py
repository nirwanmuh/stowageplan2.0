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

def plot_layout(items, Ls, Ws, cog_x, cog_y):

    fig, ax = plt.subplots(figsize=(50,14))
    ax.set_facecolor("#f0f0f0")
    fig.patch.set_facecolor("#111111")

    # Deck
    ax.add_patch(patches.Rectangle((0,0), Ls, Ws,
                                   fill=False, edgecolor='black', linewidth=4))

    # CoG lines
    ax.axvline(cog_x, color="blue", linestyle="--", linewidth=3)
    ax.axhline(cog_y, color="blue", linestyle="--", linewidth=3)

    for v in items:

        vx = v["pos"][0] + Ls/2
        vy = v["pos"][1] + Ws/2

        # clamp
        vx = max(v["length"]/2, min(Ls - v["length"]/2, vx))
        vy = max(v["width"]/2,  min(Ws - v["width"]/2,  vy))

        c = COLOR.get(v["name"], "cyan")

        ax.add_patch(
            patches.Rectangle(
                (vx - v["length"]/2, vy - v["width"]/2),
                v["length"], v["width"],
                fill=True, edgecolor=c, facecolor=c, alpha=0.5, linewidth=3
            )
        )
        ax.text(vx, vy, v["name"], fontsize=20, ha="center", weight="bold")

    cx, cy = compute_cog(items)
    ax.scatter(cx + Ls/2, cy + Ws/2, s=300, color="red")
    ax.text(cx + Ls/2, cy + Ws/2, "CoG", fontsize=22, weight="bold", color="red")

    ax.set_xlim(0, Ls)
    ax.set_ylim(0, Ws)
    ax.set_aspect("equal")

    return fig
