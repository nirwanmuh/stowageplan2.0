import streamlit as st
import json
from utils.stowage import auto_arrange, compute_cog
from utils.layout import plot_layout

st.set_page_config(layout="wide")
st.title("Stowage Plan Ferry (Free Placement)")

L = st.number_input("Panjang kapal (meter)", 40.0)
W = st.number_input("Lebar kapal (meter)", 12.0)

empty_cog_x = st.number_input("CoG kapal kosong (X)", 0.0)
empty_cog_y = W / 2
st.write("CoG kapal kosong Y =", empty_cog_y)

with open("data/vehicles.json") as f:
    VEHICLES = json.load(f)

vehicle = st.selectbox("Pilih Golongan Kendaraan", list(VEHICLES.keys()))

if "items" not in st.session_state:
    st.session_state["items"] = []

if st.button("Tambahkan Kendaraan"):
    v = VEHICLES[vehicle].copy()
    v["name"] = vehicle
    st.session_state["items"].append(v)

    st.session_state["items"] = auto_arrange(
        st.session_state["items"],
        L,
        W,
        empty_cog_x,
        empty_cog_y
    )

items = st.session_state["items"]
if len(items) > 0:
    fig = plot_layout(items, L, W, empty_cog_x, empty_cog_y)
    st.pyplot(fig, use_container_width=True)
else:
    st.write("Belum ada kendaraan.")
