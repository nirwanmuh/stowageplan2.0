import streamlit as st
import json
from utils.stowage import auto_arrange, compute_cog
from utils.layout import plot_layout

st.title("Stowage Plan Ferry (Free Placement)")

# Input kapal
L = st.number_input("Panjang kapal (meter)", 40.0)
W = st.number_input("Lebar kapal (meter)", 12.0)

# Load data kendaraan
with open("data/vehicles.json") as f:
    VEHICLES = json.load(f)

# Select kendaraan
vehicle = st.selectbox("Pilih Golongan Kendaraan", list(VEHICLES.keys()))

# Pastikan session_state.items SELALU list
if "items" not in st.session_state or not isinstance(st.session_state.items, list):
    st.session_state.items = []

# Tombol tambah
if st.button("Tambahkan Kendaraan"):
    new_vehicle = VEHICLES[vehicle].copy()
    new_vehicle["name"] = vehicle

    # Append
    st.session_state.items.append(new_vehicle)

    # Safe arrange
    arranged = auto_arrange(st.session_state.items, L, W)

    # Jika arrange gagal → fallback
    if not isinstance(arranged, list):
        arranged = st.session_state.items

    st.session_state.items = arranged

# Tampilkan hasil
if st.session_state.items:
    fig = plot_layout(st.session_state.items, L, W)
    st.pyplot(fig)
    st.write("Center of Gravity:", compute_cog(st.session_state.items))
else:
    st.write("Belum ada kendaraan.")
