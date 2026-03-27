import streamlit as st
import json
from utils.stowage import GA_arrange
from utils.layout import plot_layout

st.set_page_config(layout="wide")
st.title("Stowage Plan Ferry — Genetic Algorithm (GA) Version")

L = st.number_input("Panjang kapal (meter)", 40.0)
W = st.number_input("Lebar kapal (meter)", 12.0)

cog_x = st.number_input("CoG Kapal X", 10.0)
cog_y = W/2

with open("data/vehicles.json") as f:
    VEHICLES = json.load(f)

if "vehicles" not in st.session_state:
    st.session_state["vehicles"] = []

vehicle = st.selectbox("Pilih Kendaraan", list(VEHICLES.keys()))

if st.button("Tambah"):
    v = VEHICLES[vehicle].copy()
    v["name"] = vehicle
    st.session_state["vehicles"].append(v)

if st.button("Generate GA Layout"):
    st.session_state["vehicles"] = GA_arrange(
        st.session_state["vehicles"],
        L, W,
        cog_x, cog_y
    )

items = st.session_state["vehicles"]

if len(items) > 0:
    fig = plot_layout(items, L, W, cog_x, cog_y)
    st.pyplot(fig, use_container_width=True)
else:
    st.write("Belum ada kendaraan.")
