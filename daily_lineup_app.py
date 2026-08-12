import streamlit as st
import dropbox
import json
from datetime import datetime, timedelta
import lineup_config as cfg

st.set_page_config(page_title="The Daily Lineup", page_icon="🏅", layout="centered")

DROPBOX_PATH = "/CTS-Family/daily-lineup-state.json"
dbx = cfg.get_dbx()

def load_state():
    try:
        _, res = dbx.files_download(DROPBOX_PATH)
        return json.loads(res.content)
    except Exception:
        return {"days": {}}

def save_state(state):
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
.dot { width:12px; height:12px; border-radius:50%; background:#2A3D68; margin:6px auto 0; }
.dot-done { background:#4CAF6D; }
.small-note { font-family:'Space Mono', monospace; font-size:12px; color:#B9C0D4; }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# CHECKLIST DEFINITIONS
# ---------------------------------------------------------------------------
_lineup = cfg.load_config()
AM_REQUIRED = _lineup["am_required"]
AM_SPORT = _lineup["am_sport"]
AM_LAST = _lineup["am_last"]
AM_BONUS = _lineup["am_bonus"]
AFTER_REQUIRED = _lineup["after_required"]
AFTER_BONUS = _lineup["after_bonus"]
PM_REQUIRED = _lineup["pm_required"]
COACH_REQUIRED = _lineup["coach_required"]
WEEK_LABELS = ["M", "T", "W", "T", "F"]

# ---------------------------------------------------------------------------
# STATE
# ---------------------------------------------------------------------------
if "full_state" not in st.session_state:
    st.session_state.full_state = load_state()

today = datetime.now()
today_iso = today.strftime("%Y-%m-%d")
monday = today - timedelta(days=today.weekday())
week_dates = [(monday + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(5)]

day_state = st.session_state.full_state["days"].setdefault(today_iso, {
    "am": {}, "after": {}, "pm": {}, "gameday": False, "pm_complete": False,
})

def persist():
    save_state(st.session_state.full_state)

# ---------------------------------------------------------------------------
# HEADER
# ---------------------------------------------------------------------------
st.title("The Daily Lineup")
st.caption("4th grade season · have-tos before bonus round")

gameday = st.toggle("Game or practice today?", value=day_state.get("gameday", False))
if gameday != day_state.get("gameday", False):
    day_state["gameday"] = gameday
    persist()

st.markdown("<div class='small-note'>This week's closing lineup</div>", unsafe_allow_html=True)
cols = st.columns(5)
for i, wd in enumerate(week_dates):
    done = st.session_state.full_state["days"].get(wd, {}).get("pm_complete", False)
    is_today = (wd == today_iso)
    classes = "streak-box" + (" streak-done" if done else "") + (" streak-today" if is_today else "")
    dot_class = "dot dot-done" if done else "dot"
    cols[i].markdown(f"<div class='{classes}'>{WEEK_LABELS[i]}<div class='{dot_class}'></div></div>", unsafe_allow_html=True)

st.divider()

# ---------------------------------------------------------------------------
# TABS
# ---------------------------------------------------------------------------
tab_am, tab_after, tab_pm, tab_coach = st.tabs(["AM · Warm-up", "Clinic · Halftime", "PM · Cool-down", "Coach"])

def checklist_block(section_key, items, day_dict, prefix):
    done_count = 0
    for i, label in enumerate(items):
        key = f"{prefix}{i}"
        checked = st.checkbox(label, value=day_dict.get(key, False), key=f"{today_iso}-{section_key}-{key}")
        if checked != day_dict.get(key, False):
            day_dict[key] = checked
            persist()
        if checked:
            done_count += 1
    return done_count

with tab_am:
    st.subheader("Starting lineup — have to")
    am_items = AM_REQUIRED + (AM_SPORT if gameday else []) + AM_LAST
    done = checklist_block("am", am_items, day_state["am"], "req")
    total = len(am_items)
    st.progress(done / total if total else 0, text=f"{done} / {total}")

    st.subheader("Bonus round — want to, if time's left")
    if done == total and total > 0:
        checklist_block("am", AM_BONUS, day_state["am"], "bonus")
    else:
        st.caption("Finish the starting lineup to unlock.")

with tab_after:
    st.subheader("Halftime lineup — have to, at the clinic")
    done = checklist_block("after", AFTER_REQUIRED, day_state["after"], "req")
    total = len(AFTER_REQUIRED)
    st.progress(done / total if total else 0, text=f"{done} / {total}")

    st.subheader("Bonus round — want to, if time's left")
    if done == total and total > 0:
        checklist_block("after", AFTER_BONUS, day_state["after"], "bonus")
    else:
        st.caption("Finish the halftime lineup to unlock.")

with tab_pm:
    st.subheader("Closing lineup — have to, after practice/game")
    done = checklist_block("pm", PM_REQUIRED, day_state["pm"], "req")
    total = len(PM_REQUIRED)
    st.progress(done / total if total else 0, text=f"{done} / {total}")

    complete = (done == total and total > 0)
    if complete != day_state.get("pm_complete", False):
        day_state["pm_complete"] = complete
        persist()

    st.subheader("Friday only, if the week was a success")
    mon_thu_done = all(
        st.session_state.full_state["days"].get(wd, {}).get("pm_complete", False)
        for wd in week_dates[:4]
    )
    friday_done = st.session_state.full_state["days"].get(week_dates[4], {}).get("pm_complete", False)
    week_success = mon_thu_done and friday_done
    if week_success:
        st.checkbox("Choose Friday night dinner", key=f"{today_iso}-friday-dinner")
        st.success("Week complete — Friday dinner pick unlocked.")
    else:
        done_count = sum(
            st.session_state.full_state["days"].get(wd, {}).get("pm_complete", False)
            for wd in week_dates
        )
        st.caption(f"This week: {done_count} / 5 closing lineups done. Needs all 5 to unlock.")

with tab_coach:
    st.subheader("Coach's list — your own routine")
    coach_state = st.session_state.full_state["days"][today_iso].setdefault("coach", {})
    checklist_block("coach", COACH_REQUIRED, coach_state, "req")
    st.caption('Doing this next to his list, out loud, is the point — not checking it perfectly.')
