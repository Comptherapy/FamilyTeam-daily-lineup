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

[data-testid="stCheckbox"] label p
