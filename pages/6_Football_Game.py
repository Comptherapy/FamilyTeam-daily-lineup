import streamlit as st
import lineup_config as cfg

st.set_page_config(page_title="Football Game", page_icon="🏈", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Oswald:wght@600;700&display=swap');
.stApp { background-color: #0F1A30; color: #F4F1EA; }
h1, h2, h3 { font-family: 'Oswald', sans-serif !important; text-transform: uppercase; letter-spacing: 0.5px; }
</style>
""", unsafe_allow_html=True)

st.title("Football game")
st.caption("Gear check — before you walk out the door")

ITEMS = cfg.load_config()["sport_football_game"]

done = 0
for i, item in enumerate(ITEMS):
    checked = st.checkbox(item, key=f"fb_game_{i}")
    if checked:
        done += 1
st.progress(done / len(ITEMS) if ITEMS else 0, text=f"{done} / {len(ITEMS)}")
