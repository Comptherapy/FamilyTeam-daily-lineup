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
# CHECKLIST DEFINITIONS — loaded from Dropbox via lineup_config.py
# Edit these anytime from the "Manage Lineup" page in the sidebar.
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

def section_header(tag_text, tag_class, title_text):
    st.markdown(
        f'<div class="section-header-wrap">'
        f'<span class="section-tag {tag_class}">{tag_text}</span>'
        f'<h3 style="margin:6px 0 0 0;">{title_text}</h3>'
        f'</div>',
        unsafe_allow_html=True,
    )

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
    section_header("STARTING LINEUP", "tag-lineup", "Have to")
    am_items = AM_REQUIRED + (AM_SPORT if gameday else []) + AM_LAST
    done = checklist_block("am", am_items, day_state["am"], "req")
    total = len(am_items)
    st.progress(done / total if total else 0, text=f"{done} / {total}")

    section_header("BONUS ROUND", "tag-bonus", "Want to, if time's left")
    if done == total and total > 0:
        checklist_block("am", AM_BONUS, day_state["am"], "bonus")
    else:
        st.caption("Finish the starting lineup to unlock.")

with tab_after:
    section_header("HALFTIME LINEUP", "tag-lineup", "Have to, at the clinic")
    done = checklist_block("after", AFTER_REQUIRED, day_state["after"], "req")
    total = len(AFTER_REQUIRED)
    st.progress(done / total if total else 0, text=f"{done} / {total}")

    section_header("BONUS ROUND", "tag-bonus", "Want to, if time's left")
    if done == total and total > 0:
        checklist_block("after", AFTER_BONUS, day_state["after"], "bonus")
    else:
        st.caption("Finish the halftime lineup to unlock.")

with tab_pm:
    section_header("CLOSING LINEUP", "tag-lineup", "Have to, after practice/game")
    done = checklist_block("pm", PM_REQUIRED, day_state["pm"], "req")
    total = len(PM_REQUIRED)
    st.progress(done / total if total else 0, text=f"{done} / {total}")

    complete = (done == total and total > 0)
    if complete != day_state.get("pm_complete", False):
        day_state["pm_complete"] = complete
        persist()

    section_header("FRIDAY ONLY", "tag-bonus", "If the week was a success")
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
    section_header("COACH'S LIST", "tag-lineup", "Your own routine")
    coach_state = st.session_state.full_state["days"][today_iso].setdefault("coach", {})
    checklist_block("coach", COACH_REQUIRED, coach_state, "req")
    st.caption('Doing this next to his list, out loud, is the point — not checking it perfectly.')
