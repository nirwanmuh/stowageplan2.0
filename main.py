import streamlit as st
import json
from utils.stowage import auto_arrange, compute_cog, optimize_positions
from utils.layout import plot_layout

st.set_page_config(layout="wide")
st.title("Stowage Plan Ferry (Optimized CoG Placement)")

# ==========================
# INPUT DECK SIZE
# ==========================
L = st.number_input("Panjang kapal (meter)", 40.0)
W = st.number_input("Lebar kapal (meter)", 12.0)

# ==========================
# INPUT COG KAPAL
# ==========================
empty_cog_x = st.number_input("CoG kapal (X)", 10.0)
empty_cog_y = W / 2
st.write("CoG kapal (Y) =", empty_cog_y)

# ==========================
# LOAD VEHICLE DATABASE
# ==========================
with open("data/vehicles.json") as f:
    VEHICLES = json.load(f)

vehicle = st.selectbox("Pilih Golongan Kendaraan", list(VEHICLES.keys()))

# ==========================
# SESSION STATE (SAFE)
# ==========================
if "items" not in st.session_state or not isinstance(st.session_state.items, list):
    st.session_state.items = []

items = st.session_state.items

# ==========================
# ADD VEHICLE
# ==========================
if st.button("Tambahkan Kendaraan"):

    # Safety guard
    if not isinstance(st.session_state.items, list):
        st.session_state.items = []

    v = VEHICLES[vehicle].copy()
    v["name"] = vehicle
    st.session_state.items.append(v)

    # STEP 1 — initial placement near CoG
    arranged = auto_arrange(
        st.session_state.items,
        L, W,
        empty_cog_x,
        empty_cog_y
    )

    # STEP 2 — optimization (swap positions)
    target_x_center = empty_cog_x - L/2
    target_y_center = empty_cog_y - W/2

    optimized = optimize_positions(
        arranged,
        L, W,
        target_x_center,
        target_y_center,
        iterations=300
    )

    st.session_state.items = optimized

# ==========================
# DRAW RESULTS
# ==========================
items = st.session_state.items

if not isinstance(items, list):
    items = []
    st.session_state.items = []

if len(items) > 0:
    fig = plot_layout(items, L, W, empty_cog_x, empty_cog_y)
    st.pyplot(fig, use_container_width=True)

    st.write("CoG kendaraan saat ini:", compute_cog(items))
else:
    st.write("Belum ada kendaraan.")
