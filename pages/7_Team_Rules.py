import streamlit as st
import theme

st.set_page_config(page_title="Team Rules", page_icon="📋", layout="centered")
st.markdown(theme.CSS, unsafe_allow_html=True)

theme.sport_hero(theme.referee_icon(110), "Team Rules", "Read this anytime — this is the deal we made with each other.")

st.markdown(
    "Listen up. Every good team runs on two things: everybody knows their job, "
    "and everybody trusts everybody else to do theirs. That's it. That's the whole "
    "system. This isn't a list of rules — it's the deal we're making with each "
    "other so mornings and evenings stop being a fight and start being just... "
    "what we do. You've got a job. I've got a job. We both show up for it. Let's go."
)

theme.section_header("COACH'S WARM-UP", "tag-lineup", "What Mom brings every day")
st.markdown(
    "- I will always love you, keep you safe, feed you, help you learn, and take care of you — no matter what.\n"
    "- I run my own lineup too, on the Coach tab — so you're never the only one doing the work.\n"
    "- When the lineup's done, I back you up on the bonus round. No moving goalposts."
)

theme.section_header("YOUR POSITION", "tag-lineup", "The starting lineup")
st.markdown(
    "- **Morning:** wake up, get ready, and be in the car on time — full list on the AM tab.\n"
    "- **Afterschool:** homework, reading, and a snack at the clinic — full list on the Clinic tab.\n"
    "- **Evening:** everything to close out the day — full list on the PM tab.\n"
    "- **Weekends:** help with your chores when Mom asks."
)

theme.section_header("GAME RULES", "tag-bonus", "Bonus round privileges")
st.markdown(
    "- **Morning:** SportsCenter, free time.\n"
    "- **Afterschool:** playtime at the clinic, screen time.\n"
    "- **Friday, if the whole week's clean:** you pick Friday night dinner.\n\n"
    "Bonus round only opens once the starting lineup's finished — same as any game, "
    "you play your position before you get the extras."
)

theme.section_header("AGREEMENT", "tag-lineup", "We're on the same team")
st.markdown(
    "You play your position, I'll play mine, and we keep getting better at this "
    "together — all season long."
)
