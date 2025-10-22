import streamlit as st
import json
import openai

# ===============================
# APP CONFIGURATION
# ===============================
APP_NAME = "AI Bayan for TS — Smart English Trainer"
st.set_page_config(page_title=APP_NAME, page_icon="🤖", layout="wide")

# ===============================
# LOGO AND HEADER
# ===============================
LOGO_URL = "https://raw.githubusercontent.com/aiko030500-wq/top-star-bayan/main/assets/ai_bayan_logo.png"

try:
    st.sidebar.image(LOGO_URL, use_container_width=True)
except Exception as e:
    st.sidebar.warning("⚠️ Couldn't load logo from GitHub URL.")
st.sidebar.title("👧 AI Bayan for TS")
st.sidebar.markdown("Smart English Trainer for students in Kazakhstan 🇰🇿")

# ===============================
# LOAD CURRICULUM
# ===============================
try:
    with open("data/curriculum.json", "r", encoding="utf-8") as f:
        curriculum = json.load(f)
except Exception:
    curriculum = {"units": []}
    st.warning("⚠️ Curriculum file not found or invalid. Please check data/curriculum.json")

# ===============================
# APP MENU
# ===============================
sections = [
    "Vocabulary",
    "Grammar",
    "Reading",
    "Listening",
    "Speaking",
    "Writing",
    "Games",
    "Progress",
    "AI-Chat Bayan"
]

section = st.sidebar.radio("📚 Choose a section:", sections)

# ===============================
# PAGE TITLE
# ===============================
st.title("👧 AI Bayan for TS — Smart English Trainer")
st.write("Learn English with **AI Bayan** — your interactive AI assistant for TS students 🇰🇿")

# ===============================
# SECTION LOGIC
# ===============================

if section == "Vocabulary":
    st.header("📖 Vocabulary Practice")
    if curriculum["units"]:
        for word in curriculum["units"][0]["vocabulary"]:
            st.markdown(f"**{word['word']}** — {word['translation']}")
            st.caption(f"Example: {word['example']}")
    else:
        st.info("No vocabulary data found yet.")

elif section == "Grammar":
    st.header("✏️ Grammar Exercises")
    if curriculum["units"]:
        grammar = curriculum["units"][0]["grammar"]
        st.subheader(grammar["topic"])
        for ex in grammar["exercises"]:
            st.text_input(ex["question"], key=ex["question"])
    else:
        st.info("No grammar data found yet.")

elif section == "Reading":
    st.header("📚 Reading Practice")
    if curriculum["units"]:
        text = curriculum["units"][0]["reading"]
        st.write(text["text_en"])
        st.caption(text["text_ru"])
    else:
        st.info("No reading data found yet.")

elif section == "Listening":
    st.header("🎧 Listening Practice")
    if curriculum["units"]:
        listen = curriculum["units"][0]["listening"]
        st.write(listen["script_en"])
        st.caption(listen["script_ru"])
    else:
        st.info("No listening data found yet.")

elif section == "Speaking":
    st.header("🗣️ Speaking Practice")
    if curriculum["units"]:
        for task in curriculum["units"][0]["speaking_prompts"]:
            st.markdown(f"- {task}")
    else:
        st.info("No speaking prompts found yet.")

elif section == "Writing":
    st.header("✍️ Writing Practice")
    if curriculum["units"]:
        for task in curriculum["units"][0]["writing_tasks"]:
            st.markdown(f"- {task}")
    else:
        st.info("No writing tasks found yet.")

elif section == "Games":
    st.header("🎮 English Games")
    st.info("Fun interactive games will be added soon! 💫")

elif section == "Progress":
    st.header("🌟 Progress Tracker")
    st.info("Track your achievements and stars ⭐")

# ===============================
# AI-CHAT BAYAN SECTION
# ===============================
elif section == "AI-Chat Bayan":
    st.header("🤖 AI-Chat Bayan — Ask and Learn")

    user_input = st.text_input("Type your question or answer in English:")

    if st.button("Ask Bayan"):
        if user_input.strip():
            try:
                openai.api_key = st.secrets["OPENAI_API_KEY"]
                response = openai.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are Bayan, a kind and patient English teacher for 4th grade students in Kazakhstan. Speak simply and clearly."},
                        {"role": "user", "content": user_input}
                    ]
                )
                st.success(response.choices[0].message.content)
            except Exception as e:
                st.error("⚠️ Error: " + str(e))
        else:
            st.warning("Please enter your message first.")
