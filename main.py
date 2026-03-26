import streamlit as st
import json
from utils.stowage import auto_arrange, compute_cog
from utils.layout import plot_layout

st.title("Stowage Plan Ferry (Free Placement)")

L = st.number_input("Panjang kapal (meter)", 40.0)
W = st.number_input("Lebar kapal (meter)", 12.0)

with open("data/vehicles.json") as f:
    VEHICLES = json.load(f)

vehicle = st.selectbox("Pilih Golongan Kendaraan", VEHICLES.keys())

# session
if "items" not in st.session_state:
    st.session_state.items = []

if st.button("Tambahkan Kendaraan"):
    v = VEHICLES[vehicle].copy()
    v["name"] = vehicle  # beri nama untuk label
    st.session_state.items.append(v)

    # pastikan result selalu list
    arranged = auto_arrange(st.session_state.items, L, W)
    
    # jika auto_arrange return None → fallback list kosong
    if arranged is None:
        arranged = []

    st.session_state.items = arranged

# render
if st.session_state.items:
    fig = plot_layout(st.session_state.items, L, W)
    st.pyplot(fig)
    st.write("Center of Gravity:", compute_cog(st.session_state.items))
else:
    st.write("Belum ada kendaraan.")
