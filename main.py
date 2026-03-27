import streamlit as st
import json
from utils.stowage import auto_arrange
from utils.layout import plot_layout

st.set_page_config(layout="wide")
st.title("Stowage Plan Ferry – NO OVERLAP, AABB-BASED")

L = st.number_input("Panjang kapal (m)", 40.0)
W = st.number_input("Lebar kapal (m)", 12.0)

empty_cog_x = st.number_input("CoG kapal X", 10.0)
empty_cog_y = W/2

with open("data/vehicles.json") as f:
    VEHICLES = json.load(f)

if "items" not in st.session_state:
    st.session_state["items"] = []

vehicle = st.selectbox("Pilih kendaraan", list(VEHICLES.keys()))

if st.button("Tambahkan"):
    v = VEHICLES[vehicle].copy()
    v["name"] = vehicle
    st.session_state["items"].append(v)

    arranged = auto_arrange(
        st.session_state["items"], L, W,
        empty_cog_x, empty_cog_y
    )

    st.session_state["items"] = arranged

items = st.session_state["items"]

if len(items) > 0:
    fig = plot_layout(items, L, W, empty_cog_x, empty_cog_y)
    st.pyplot(fig, use_container_width=True)
