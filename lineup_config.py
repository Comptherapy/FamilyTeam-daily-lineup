import streamlit as st
import dropbox
import json

CONFIG_PATH = "/CTS-Family/lineup-config.json"

DEFAULT_CONFIG = {
    "am_required": [
        "Wake up when the alarm goes off", "Use the restroom", "Get dressed", "Put on shoes",
        "Brush teeth", "Fix hair", "Contacts in / glasses on", "Take vitamins", "Eat breakfast",
        "Backpack check: homework folder", "Water bottle packed",
    ],
    "am_sport": ["Sports items checked"],
    "am_last": ["In the car on time"],
    "am_bonus": ["Watch SportsCenter", "Free time"],
    "after_required": ["Finish homework", "Complete reading", "Eat snack"],
    "after_bonus": ["Play in the back of the clinic", "Screen time"],
    "pm_required": [
        "Clean out trash and bring in school/sport items from the car",
        "Finish any leftover homework or study", "Eat dinner", "Feed Rudy", "Shower",
        "Brush teeth", "Put dirty clothes in the hamper", "Lay out tomorrow's clothes",
        "Pack tomorrow's practice or game clothes/gear",
        "Fill water bottle and put it in the fridge", "Tidy living space",
    ],
    "coach_required": [
        "Shower", "Get ready", "Brush teeth", "Pack work items", "Eat breakfast", "Exercise",
    ],
    "sport_basketball_practice": [
        "Basketball shoes", "Practice jersey / reversible", "Athletic socks", "Shorts",
        "Mouthguard", "Water bottle, filled",
    ],
    "sport_basketball_game": [
        "Game jersey (home or away — check which)", "Game shorts", "Basketball shoes", "Socks",
        "Mouthguard", "Warm-up / hoodie", "Water bottle, filled", "Team bag",
    ],
    "sport_baseball_practice": [
        "Glove", "Bat", "Batting gloves", "Cleats", "Practice jersey", "Hat", "Water bottle, filled",
    ],
    "sport_baseball_game": [
        "Full uniform (jersey, pants, belt)", "Glove", "Bat", "Batting gloves", "Cleats",
        "Helmet", "Cup", "Hat", "Water bottle, filled",
    ],
    "sport_football_practice": [
        "Helmet", "Shoulder pads", "Practice jersey", "Cleats", "Mouthguard", "Water bottle, filled",
    ],
    "sport_football_game": [
        "Game jersey", "Helmet", "Shoulder pads", "Game pants", "Cleats", "Mouthguard",
        "Water bottle, filled",
    ],
}

SECTION_LABELS = {
    "am_required": "Morning — Starting Lineup",
    "am_sport": "Morning — Sports Gear Check (game days only)",
    "am_last": "Morning — Last Item Before Leaving",
    "am_bonus": "Morning — Bonus Round",
    "after_required": "Afterschool — Halftime Lineup",
    "after_bonus": "Afterschool — Bonus Round",
    "pm_required": "Evening — Closing Lineup",
    "coach_required": "Coach's List (Mom)",
    "sport_basketball_practice": "Basketball Practice Gear",
    "sport_basketball_game": "Basketball Game Gear",
    "sport_baseball_practice": "Baseball Practice Gear",
    "sport_baseball_game": "Baseball Game Gear",
    "sport_football_practice": "Football Practice Gear",
    "sport_football_game": "Football Game Gear",
}


@st.cache_resource
def get_dbx():
    return dropbox.Dropbox(
        app_key=st.secrets["DROPBOX_APP_KEY"],
        app_secret=st.secrets["DROPBOX_APP_SECRET"],
        oauth2_refresh_token=st.secrets["DROPBOX_REFRESH_TOKEN"],
    )


def load_config():
    dbx = get_dbx()
    try:
        _, res = dbx.files_download(CONFIG_PATH)
        config = json.loads(res.content)
        for key, value in DEFAULT_CONFIG.items():
            if key not in config:
                config[key] = value
        return config
    except Exception:
        return {k: list(v) for k, v in DEFAULT_CONFIG.items()}


def save_config(config):
    dbx = get_dbx()
    dbx.files_upload(
        json.dumps(config).encode("utf-8"),
        CONFIG_PATH,
        mode=dropbox.files.WriteMode("overwrite"),
    )
