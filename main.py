# main.py
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import json

# ------------------------------------------
# Load data kendaraan (lebar & berat hasil scraping)
# ------------------------------------------
with open("data/vehicles.json") as f:
    VEHICLES = json.load(f)

# ------------------------------------------
# Fungsi cek overlap rectangle
# ------------------------------------------
def overlap(a, b):
    ax, ay, aw, al = a
    bx, by, bw, bl = b

    return not (
        ax + al/2 < bx - bl/2 or
        ax - al/2 > bx + bl/2 or
        ay + aw/2 < by - bw/2 or
        ay - aw/2 > by + bw/2
    )

# ------------------------------------------
# Auto placement bebas
# ------------------------------------------
def auto_arrange(items, L, W):
    # Sort by weight (desc)
    items.sort(key=lambda x: -x["weight"])

    radius_step = min(L, W) * 0.1
    angle_step = np.radians(30)
    r = 0
    theta = 0

    placed = []

    for v in items:
        attempt = 0
        while True:
            # Generate posisi
            x = r * np.cos(theta)
            y = r * np.sin(theta)

            rect = (x, y, v["width"], v["length"])

            # Cek overlap
            ok = True
            for p in placed:
                rect2 = (p["pos"][0], p["pos"][1], p["width"], p["length"])
                if overlap(rect, rect2):
                    ok = False
                    break

            # Cek batas kapal
            if not (-L/2 <= x <= L/2 and -W/2 <= y <= W/2):
                ok = False

            if ok:
                v["pos"] = (x, y)
                placed.append(v)
                break

            # Perbaiki posisi: tambah θ
            theta += angle_step
            if theta >= 2*np.pi:
                theta = 0
                r += radius_step

            attempt += 1
            if attempt > 5000:
                st.warning("Gagal menemukan posisi bebas.")
                break

    return placed

# ------------------------------------------
# Hitung CoG
# ------------------------------------------
def compute_cog(items):
    total_w = sum(v["weight"] for v in items)
    X = sum(v["pos"][0] * v["weight"] for v in items) / total_w
    Y = sum(v["pos"][1] * v["weight"] for v in items) / total_w
    return (X, Y)

# ------------------------------------------
# Plot Layout
# ------------------------------------------
def plot_layout(items, L, W):
    fig, ax = plt.subplots(figsize=(10, 5))

    ax.add_patch(
        patches.Rectangle((-L/2, -W/2), L, W, fill=False, linewidth=2)
    )

    for v in items:
        x, y = v["pos"]
        ax.add_patch(
            patches.Rectangle((x - v["length"]/2, y - v["width"]/2),
                              v["length"], v["width"],
                              fill=False, edgecolor="blue")
        )
        ax.text(x, y, v["name"], ha="center", fontsize=7)

    cx, cy = compute_cog(items)
    ax.scatter(cx, cy, color='red')
    ax.text(cx, cy, "CoG", color="red")

    ax.set_xlim(-L/2, L/2)
    ax.set_ylim(-W/2, W/2)
    ax.set_aspect("equal")
    return fig

# ------------------------------------------
# Streamlit UI
# ------------------------------------------
st.title("Stowage Plan Ferry (Free Placement)")

L = st.number_input("Panjang kapal (m)", 40.0)
W = st.number_input("Lebar kapal (m)", 12.0)

vehicle = st.selectbox("Pilih golongan kendaraan", VEHICLES.keys())

if "items" not in st.session_state:
    st.session_state.items = []

if st.button("Tambahkan kendaraan"):
    v = VEHICLES[vehicle].copy()
    st.session_state.items.append(v)

    st.session_state.items = auto_arrange(st.session_state.items, L, W)

if st.session_state.items:
    fig = plot_layout(st.session_state.items, L, W)
    st.pyplot(fig)
    st.write("Center of Gravity:", compute_cog(st.session_state.items))
``
