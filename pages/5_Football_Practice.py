import streamlit as st
import lineup_config as cfg
import theme

st.set_page_config(page_title="Football Practice", page_icon="🏈", layout="centered")
st.markdown(theme.CSS, unsafe_allow_html=True)

st.title("Football practice")
st.caption("Gear check — before you walk out the door")

ITEMS = cfg.load_config()["sport_football_practice"]

done = 0
for i, item in enumerate(ITEMS):
    checked = st.checkbox(item, key=f"fb_practice_{i}")
    if checked:
        done += 1
st.progress(done / len(ITEMS) if ITEMS else 0, text=f"{done} / {len(ITEMS)}")
