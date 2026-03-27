import streamlit as st
import json
from utils.stowage import auto_arrange, compute_cog, optimize_positions
from utils.layout import plot_layout

st.set_page_config(layout="wide")
st.title("Stowage Plan Ferry (NO OVERLAP FINAL)")

L = st.number_input("Panjang kapal (m)", 40.0)
W = st.number_input("Lebar kapal (m)", 12.0)

empty_cog_x = st.number_input("CoG kapal X", 10.0)
empty_cog_y = W/2
st.write("CoG kapal Y =", empty_cog_y)

with open("data/vehicles.json") as f:
    VEHICLES = json.load(f)

vehicle = st.selectbox("Pilih golongan kendaraan", list(VEHICLES.keys()))

if "items_list" not in st.session_state:
    st.session_state["items_list"] = []

items = st.session_state["items_list"]

if st.button("Tambahkan Kendaraan"):
    v = VEHICLES[vehicle].copy()
    v["name"] = vehicle
    items.append(v)

    arr = auto_arrange(items, L, W, empty_cog_x, empty_cog_y)
    target_x = empty_cog_x - L/2
    target_y = empty_cog_y - W/2

    opt = optimize_positions(arr, L, W, target_x, target_y, iterations=300)

    st.session_state["items_list"] = opt

items = st.session_state["items_list"]

if len(items) > 0:
    fig = plot_layout(items, L, W, empty_cog_x, empty_cog_y)
    st.pyplot(fig, use_container_width=True)
else:
    st.write("Belum ada kendaraan.")
