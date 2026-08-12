import streamlit as st
import dropbox
import json
from datetime import datetime, timedelta
import lineup_config as cfg
import theme

st.set_page_config(page_title="The Daily Lineup", page_icon="🏅", layout="centered")
st.markdown(theme.CSS, unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# DROPBOX SETUP (daily state — checklist item text now lives in lineup_config.py)
# ---------------------------------------------------------------------------
DROPBOX_PATH = "/CTS-Family/daily-lineup-state.json"
dbx = cfg.get_dbx()

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
# CHECKLIST DEFINITIONS — loaded from Dropbox via
