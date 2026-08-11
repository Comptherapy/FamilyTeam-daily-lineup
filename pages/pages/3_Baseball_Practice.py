import streamlit as st
st.set_page_config(page_title="Baseball Practice", page_icon="⚾", layout="centered")
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Oswald:wght@600;700&display=swap');
.stApp { background-color: #0F1A30; color: #F4F1EA; }
h1, h2, h3 { font-family: 'Oswald', sans-serif !important; text-transform: uppercase; letter-spacing: 0.5px; }
</style>
""", unsafe_allow_html=True)

st.title("Baseball practice")
st.caption("Gear check — before you walk out the door")
st.caption("Starter list — tell your parent if anything's missing or extra so it can be fixed.")

ITEMS = [
    "Glove",
    "Bat",
    "Batting gloves",
    "Cleats",
    "Practice jersey",
    "Hat",
    "Water bottle, filled",
]

done = 0
for i, item in enumerate(ITEMS):
    checked = st.checkbox(item, key=f"bs_practice_{i}")
    if checked:
        done += 1
st.progress(done / len(ITEMS) if ITEMS else 0, text=f"{done} / {len(ITEMS)}")
