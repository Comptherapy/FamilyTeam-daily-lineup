import streamlit as st
import lineup_config as cfg
import theme

st.set_page_config(page_title="Manage Lineup", page_icon="🛠️", layout="centered")
st.markdown(theme.CSS, unsafe_allow_html=True)

st.title("Manage the lineup")
st.caption("Add, remove, or update items here — changes apply immediately everywhere in the app.")

config = cfg.load_config()

section_key = st.selectbox(
    "Which list do you want to edit?",
    options=list(cfg.SECTION_LABELS.keys()),
    format_func=lambda k: cfg.SECTION_LABELS[k],
)

items = config.get(section_key, [])
st.subheader(cfg.SECTION_LABELS[section_key])

if not items:
    st.caption("No items yet — add one below.")

for i, item in enumerate(items):
    col1, col2 = st.columns([5, 1])
    col1.write(f"• {item}")
    if col2.button("Remove", key=f"remove-{section_key}-{i}"):
        items.pop(i)
        config[section_key] = items
        cfg.save_config(config)
        st.rerun()

st.divider()

new_item = st.text_input("Add a new item", key=f"new-{section_key}")
if st.button("Add item", key=f"add-{section_key}"):
    if new_item.strip():
        items.append(new_item.strip())
        config[section_key] = items
        cfg.save_config(config)
        st.rerun()
    else:
        st.warning("Type something first.")
