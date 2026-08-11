import streamlit as st
import dropbox
import json
from datetime import datetime, timedelta

st.set_page_config(page_title="The Daily Lineup", page_icon="🏅", layout="centered")

# ---------------------------------------------------------------------------
# DROPBOX SETUP
# Reuses the same Dropbox token pattern as your other CTS Streamlit apps.
# In Streamlit Cloud -> App settings -> Secrets, add the same DROPBOX_* keys
# you already use for cts-checkin-form / cts-payment-sheet. If those apps use
# a refresh-token flow (OAuth refresh token + app key/secret) instead of a
# single long-lived token, swap the dropbox.Dropbox(...) line below for
# whatever helper/init code you already have in those repos -- the rest of
# this app doesn't care how the client is created, only that `dbx` works.
# ---------------------------------------------------------------------------
DROPBOX_PATH = "/CTS-Family/daily-lineup-state.json"

@st.cache_resource
def get_dbx():
    return dropbox.Dropbox(st.secrets["DROPBOX_TOKEN"])

dbx = get_dbx()

def load_state():
    try:
        _, res = dbx.files_download(DROPBOX_PATH)
        return json.loads(res.content)
    except Exception:
        return {"days": {}}

def save_state(state):
    # Keep only the last 21 days so the file doesn't grow forever
    cutoff = (datetime.now() - timedelta(days=21)).strftime("%Y-%m-%d")
    state["days"] = {d: v for d, v in state["days"].items() if d >= cutoff}
    dbx.files_upload(
        json.dumps(state).encode("utf-8"),
        DROPBOX_PATH,
        mode=dropbox.files.WriteMode("overwrite"),
    )

# ---------------------------------------------------------------------------
# THEME
# ---------------------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Oswald:wght@600;700&family=Space+Mono:wght@400;700&display=swap');
.stApp { background-color: #0F1A30; color: #F4F1EA; }
h1, h2, h3 { font-family: 'Oswald', sans-serif !important; text-transform: uppercase; letter-spacing: 0.5px; }
.streak-box { display:inline-block; width:14%; text-align:center; padding:8px 2px; border-radius:6px;
  border:1px solid #2A3D68; background:#1F2E52; margin-right:4px; }
.streak-done { border-color:#4CAF6D; }
.streak-today { border-color:#FFC145; }
.dot { width:12px; height:12px;
