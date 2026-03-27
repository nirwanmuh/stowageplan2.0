import streamlit as st
import json
from utils.stowage import auto_arrange, compute_cog
from utils.layout import plot_layout

st.title("Stowage Plan Ferry (Free Placement)")

# --- Input Kapal ---
L = st.number_input("Panjang kapal (meter)", 40.0)
W = st.number_input("Lebar kapal (meter)", 12.0)

# --- Load Data Kendaraan ---
with open("data/vehicles.json") as f:
    VEHICLES = json.load(f)

vehicle = st.selectbox("Pilih Golongan Kendaraan", list(VEHICLES.keys()))

# SESSION STATE FIX
if "items" not in st.session_state:
    st.session_state["items"] = []

# Jika ada korupsi state
if not isinstance(st.session_state["items"], list):
    st.session_state["items"] = []

# --- Tambah Kendaraan ---
if st.button("Tambahkan Kendaraan"):
    new_v = VEHICLES[vehicle].copy()
    new_v["name"] = vehicle

    st.session_state["items"].append(new_v)

    arranged = auto_arrange(st.session_state["items"], L, W)
    if isinstance(arranged, list):
        st.session_state["items"] = arranged
    else:
        st.session_state["items"] = st.session_state["items"]

items = st.session_state["items"]

if isinstance(items, list) and len(items) > 0:
    fig = plot_layout(items, L, W)
    st.pyplot(fig)
    st.write("Center of Gravity:", compute_cog(items))
else:
    st.write("Belum ada kendaraan.")
