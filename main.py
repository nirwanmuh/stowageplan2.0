import streamlit as st
import json
from utils.stowage import auto_arrange, compute_cog, optimize_positions
from utils.layout import plot_layout

st.set_page_config(layout="wide")
st.title("Stowage Plan Ferry (COG Optimized + No Overlap + No Cut-Off)")

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
# SAFE SESSION STATE
# ==========================
if "items_list" not in st.session_state:
    st.session_state["items_list"] = []

# hard safety
if not isinstance(st.session_state["items_list"], list):
    st.session_state["items_list"] = []

items = st.session_state["items_list"]

# ==========================
# ADD VEHICLE
# ==========================
if st.button("Tambahkan Kendaraan"):

    # safety before append
    if not isinstance(st.session_state["items_list"], list):
        st.session_state["items_list"] = []

    v = VEHICLES[vehicle].copy()
    v["name"] = vehicle
    st.session_state["items_list"].append(v)

    arranged = auto_arrange(
        st.session_state["items_list"],
        L, W,
        empty_cog_x,
        empty_cog_y
    )

    if not isinstance(arranged, list):
        arranged = st.session_state["items_list"]

    target_x_center = empty_cog_x - L/2
    target_y_center = empty_cog_y - W/2

    optimized = optimize_positions(
        arranged,
        L, W,
        target_x_center,
        target_y_center,
        iterations=300
    )

    if not isinstance(optimized, list):
        optimized = arranged

    st.session_state["items_list"] = optimized

# ==========================
# DRAW RESULTS
# ==========================
items = st.session_state["items_list"]

if not isinstance(items, list):
    items = []
    st.session_state["items_list"] = []

if len(items) > 0:
    fig = plot_layout(items, L, W, empty_cog_x, empty_cog_y)
    st.pyplot(fig, use_container_width=True)

    st.write("CoG kendaraan:", compute_cog(items))
else:
    st.write("Belum ada kendaraan.")
