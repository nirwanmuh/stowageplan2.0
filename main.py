import streamlit as st
import json
from utils.stowage import auto_arrange, compute_cog
from utils.layout import plot_layout

# Full width layout
st.set_page_config(layout="wide")

st.title("Stowage Plan Ferry (Free Placement)")

# --- Input Kapal ---
L = st.number_input("Panjang kapal (meter)", 40.0)
W = st.number_input("Lebar kapal (meter)", 12.0)

# --- Input CoG Kapal Kosong ---
empty_cog_x = st.number_input("CoG kapal kosong (sumbu X)", 0.0)
empty_cog_y = W / 2
st.write("CoG kapal kosong (sumbu Y otomatis):", empty_cog_y)

# --- Load Data Kendaraan ---
with open("data/vehicles.json") as f:
    VEHICLES = json.load(f)

vehicle = st.selectbox("Pilih Golongan Kendaraan", list(VEHICLES.keys()))

# --- Session State ---
if "items" not in st.session_state:
    st.session_state["items"] = []

# --- Tambah Kendaraan ---
if st.button("Tambahkan Kendaraan"):
    v = VEHICLES[vehicle].copy()
    v["name"] = vehicle
    st.session_state["items"].append(v)

    arranged = auto_arrange(st.session_state["items"], L, W)
    if isinstance(arranged, list):
        st.session_state["items"] = arranged

# --- Hitung CoG kendaraan (tanpa berat kosong) ---
items = st.session_state["items"]

if len(items) > 0:
    cog = compute_cog(items)
    st.write("CoG kendaraan (X,Y):", cog)

    fig = plot_layout(items, L, W, empty_cog_x, empty_cog_y)
    st.pyplot(fig, use_container_width=True)
else:
    st.write("Belum ada kendaraan.")
