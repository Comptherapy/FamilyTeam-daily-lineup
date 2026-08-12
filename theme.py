import streamlit as st

# ---------------------------------------------------------------------------
# SHARED THEME
# Bright, bold, kid-friendly palette inspired by streetwear basketball-short
# graphics (mustard, sky blue, mint, orange, black outlines, cream base).
# Change a color here and every page picks it up automatically.
# ---------------------------------------------------------------------------

CREAM = "#FFFBF3"
INK = "#1A1A1A"
INK_SOFT = "#4A4A4A"
WHITE = "#FFFFFF"
MUSTARD = "#F5B942"
SKY = "#4FB8E8"
MINT = "#6FD6A8"
ORANGE = "#F4793A"
PURPLE = "#7B3F98"
SUCCESS = "#3FAE6A"

CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Baloo+2:wght@600;700;800&family=Nunito:wght@600;700;800&display=swap');

:root {{
  --cream: {CREAM};
  --ink: {INK};
  --ink-soft: {INK_SOFT};
  --white: {WHITE};
  --mustard: {MUSTARD};
  --sky: {SKY};
  --mint: {MINT};
  --orange: {ORANGE};
  --purple: {PURPLE};
  --success: {SUCCESS};
}}

.stApp {{
  background-color: var(--cream);
  color: var(--ink);
}}

h1, h2, h3, [data-testid="stHeading"] h1, [data-testid="stHeading"] h2, [data-testid="stHeading"] h3 {{
  font-family: 'Baloo 2', sans-serif !important;
  color: var(--ink) !important;
  font-weight: 800 !important;
}}

p, span, label, div, li {{
  font-family: 'Nunito', sans-serif;
}}

[data-testid="stCheckbox"] label p {{
  font-size: 16px !important;
  font-weight: 700 !important;
}}

[data-testid="stCheckbox"] span[role="checkbox"] {{
  border: 2px solid var(--ink) !important;
  border-radius: 6px !important;
}}

.stTabs [data-baseweb="tab"] {{
  font-family: 'Baloo 2', sans-serif !important;
  font-weight: 700 !important;
  font-size: 15px !important;
}}

.section-header-wrap {{
  margin: 18px 0 10px 0;
}}

.section-tag {{
  display:inline-block; font-family:'Baloo 2', sans-serif; font-size:12px;
  padding:5px 12px; border-radius:8px; font-weight:800; border:2px solid var(--ink);
  box-shadow: 2px 2px 0 var(--ink); transform: rotate(-2deg);
}}
.tag-lineup {{ background: var(--sky); color: var(--ink); }}
.tag-bonus {{ background: var(--mustard); color: var(--ink); transform: rotate(2deg); }}

.stripe-band {{
  height: 12px;
  background: repeating-linear-gradient(
    45deg,
    var(--mustard) 0 16px,
    var(--sky) 16px 32px,
    var(--mint) 32px 48px,
    var(--orange) 48px 64px
  );
}}

.streak-box {{
  display:inline-block; width:14%; text-align:center; padding:8px 2px; border-radius:10px;
  border:2px solid var(--ink); background: var(--white); margin-right:4px;
}}
.streak-done {{ background: var(--mint); }}
.streak-today {{ border-color: var(--orange); border-width:3px; }}
.dot {{ width:12px; height:12px; border-radius:50%; background:#D8D8D8; margin:6px auto 0; }}
.dot-done {{ background: var(--success); }}
.small-note {{ font-family:'Baloo 2', sans-serif; font-size:12px; color: var(--ink-soft); }}

/* SCOREBOARD PANEL — wraps the header (title, toggle, weekly streak) */
.st-key-scoreboard_panel {{
  background: var(--ink);
  border-radius: 16px;
  padding: 20px;
  margin-bottom: 6px;
  overflow: hidden;
  border: 3px solid var(--ink);
}}
.st-key-scoreboard_panel h1 {{ color: var(--cream) !important; font-size: 34px !important; }}
.st-key-scoreboard_panel p, .st-key-scoreboard_panel span,
.st-key-scoreboard_panel label, .st-key-scoreboard_panel div {{ color: var(--cream) !important; }}
.st-key-scoreboard_panel .streak-box {{ background:#2A2A2A; border-color:#555; }}
.st-key-scoreboard_panel .streak-done {{ background: var(--mint); }}
.st-key-scoreboard_panel .streak-today {{ border-color: var(--orange); }}
.st-key-scoreboard_panel .small-note {{ color: #C9C9C9 !important; }}
.st-key-scoreboard_panel .stripe-top {{ margin: -20px -20px 16px -20px; }}
.st-key-scoreboard_panel .stripe-bottom {{ margin: 16px -20px -20px -20px; }}

/* WHITEBOARD CARD — used for the Coach tab */
.st-key-whiteboard {{
  background:
    linear-gradient(var(--white), var(--white)),
    repeating-linear-gradient(0deg, rgba(79,184,232,0.18) 0 1px, transparent 1px 28px),
    repeating-linear-gradient(90deg, rgba(79,184,232,0.18) 0 1px, transparent 1px 28px);
  border: 4px solid var(--ink);
  border-radius: 12px;
  padding: 22px 22px 10px 22px;
  margin-top: 14px;
  position: relative;
  box-shadow: 5px 5px 0 var(--ink);
}}
.st-key-whiteboard::before, .st-key-whiteboard::after {{
  content: "";
  position: absolute;
  width: 58px; height: 22px;
  background: rgba(255,255,255,0.55);
  border: 1px solid rgba(0,0,0,0.12);
}}
.st-key-whiteboard::before {{ top: -12px; left: 24px; transform: rotate(-7deg); }}
.st-key-whiteboard::after {{ top: -12px; right: 24px; transform: rotate(7deg); }}
</style>
"""


def basketball_icon(size=40, stroke="#1A1A1A"):
    """Inline SVG basketball. Pass stroke='#FFFBF3' for use on dark backgrounds."""
    return f"""
    <svg width="{size}" height="{size}" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg">
      <circle cx="24" cy="24" r="21" fill="{ORANGE}" stroke="{stroke}" stroke-width="2.5"/>
      <path d="M24 3 V45" stroke="{stroke}" stroke-width="2.5" fill="none"/>
      <path d="M3 24 H45" stroke="{stroke}" stroke-width="2.5" fill="none"/>
      <path d="M8 8 C16 16, 16 32, 8 40" stroke="{stroke}" stroke-width="2.5" fill="none"/>
      <path d="M40 8 C32 16, 32 32, 40 40" stroke="{stroke}" stroke-width="2.5" fill="none"/>
    </svg>
    """


def jersey_icon(number=15, size=40, stroke="#1A1A1A"):
    """Inline SVG jersey with a number on it — sky blue body by default."""
    return f"""
    <svg width="{size}" height="{size}" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg">
      <path d="M14 4 L7 9 L11 17 L14 14.5 V44 H34 V14.5 L37 17 L41 9 L34 4
               Q30 8.5 24 8.5 Q18 8.5 14 4 Z"
            fill="{SKY}" stroke="{stroke}" stroke-width="2.5" stroke-linejoin="round"/>
      <text x="24" y="33" font-family="Baloo 2, sans-serif" font-size="17" font-weight="800"
            text-anchor="middle" fill="{stroke}">{number}</text>
    </svg>
    """


def title_with_icon(title_text):
    """Renders the app title with a basketball + jersey icon beside it (light text, for the scoreboard panel)."""
    st.markdown(
        f'<div style="display:flex;align-items:center;gap:10px;">'
        f'{basketball_icon(56, stroke="#FFFBF3")}'
        f'{jersey_icon(15, 50, stroke="#FFFBF3")}'
        f'<h1 style="margin:0;">{title_text}</h1>'
        f'</div>',
        unsafe_allow_html=True,
    )


def section_header(tag_text, tag_class, title_text):
    """Renders a colored badge + heading, e.g. a sky-blue 'STARTING LINEUP' tag."""
    st.markdown(
        f'<div class="section-header-wrap">'
        f'<span class="section-tag {tag_class}">{tag_text}</span>'
        f'<h3 style="margin:6px 0 0 0;">{title_text}</h3>'
        f'</div>',
        unsafe_allow_html=True,
    )
