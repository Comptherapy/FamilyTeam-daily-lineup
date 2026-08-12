import streamlit as st

st.set_page_config(page_title="Basketball Game", page_icon="🏀", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Oswald:wght@600;700&display=swap');
.stApp { background-color: #0F1A30; color: #F4F1EA; }
h1, h2, h3 { font-family: 'Oswald', sans-serif !important; text-transform: uppercase; letter-spacing: 0.5px; }
</style>
""", unsafe_allow_html=True)

st.title("Basketball game")
st.caption("Gear check — before you walk out the door")
st.caption("Starter list — tell your parent if anything's missing or extra so it can be fixed.")

ITEMS = [
    "Game jersey (home or away — check which)",
    "Game shorts",
    "Basketball shoes",
    "Socks",
    "Mouthguard",
    "Warm-up / hoodie",
    "Water bottle, filled",
    "Team bag",
]

done = 0
for i, item in enumerate(ITEMS):
    checked = st.checkbox(item, key=f"bb_game_{i}")
    if checked:
        done += 1
st.progress(done / len(ITEMS) if ITEMS else 0, text=f"{done} / {len(ITEMS)}")
