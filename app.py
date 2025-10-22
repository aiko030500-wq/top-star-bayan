st.set_page_config(page_title=APP_NAME, page_icon="🤖", layout="wide")
import json, random, pathlib, time
import streamlit as st
import json
import openai

APP_NAME = "AI Bayan for TS — Smart English Trainer"

st.title("👧 AI Bayan for TS — Smart English Trainer")
st.write("Learn English with AI Bayan — your interactive and friendly trainer for TS students 🇰🇿")
DATA_PATH = pathlib.Path(__file__).parent / "data" / "curriculum.json"
LOGO_PATH = "assets/ai_bayan_logo.png"
APP_NAME = "AI Bayan for TS — Smart English Trainer"
st.set_page_config(page_title=APP_NAME, page_icon="⭐", layout="wide")

# ---- Sidebar (logo + profile) ----
with open(LOGO_PATH, "r", encoding="utf-8") as f:
    svg_logo = f.read()
st.sidebar.markdown(svg_logo, unsafe_allow_html=True)

st.sidebar.markdown("## 👤 Student Profile")
student_name = st.sidebar.text_input("Введите своё имя / Enter your name:", value="")
grade = st.sidebar.selectbox("Класс / Grade:", ["4 «A»", "4 «B»", "4 «C»", "Other"])
lang = st.sidebar.radio("Interface Language:", ["English", "Русский"], index=1)

st.sidebar.markdown("---")
st.sidebar.caption("Created by Bayan · School №6 · Kazakhstan")

# Persistent session state
if "stars" not in st.session_state:
    st.session_state.stars = 0
if "completed" not in st.session_state:
    st.session_state.completed = set()

# ---- Load curriculum ----
with open(DATA_PATH, "r", encoding="utf-8") as f:
    curriculum = json.load(f)

units = curriculum["units"]
unit_titles = [f"Unit {u['id']}: {u['title_en']}" for u in units]
unit_idx = st.sidebar.selectbox("Select Unit / Выберите юнит:", list(range(len(units))), format_func=lambda i: unit_titles[i])

# Main navigation (8 sections)
sections = [
    "Vocabulary",
    "Grammar",
    "Reading",
    "Listening",
    "Speaking",
    "Writing",
    "Games",
    "Progress",
]
choice = st.sidebar.radio("📚 Sections / Разделы", sections, index=0)

unit = units[unit_idx]

def award_star(n=1):
    st.session_state.stars += n
    st.balloons()
    st.success(f"+{n} ⭐ Good job! Молодец!")

# ---- Helpers ----
def header_title():
    if lang == "Русский":
        st.title(f"⭐ {APP_NAME}")
        st.subheader(f"Юнит {unit['id']}: {unit['title_ru']} · Ученик: {student_name or '—'}")
    else:
        st.title(f"⭐ {APP_NAME}")
        st.subheader(f"Unit {unit['id']}: {unit['title_en']} · Student: {student_name or '—'}")

def check_answer(user, correct):
    return user.strip().lower() == correct.strip().lower()

# ---- Vocabulary ----
def page_vocabulary():
    header_title()
    st.markdown("### 📖 Vocabulary / Словарь")
    cols = st.columns(2)
    for i, item in enumerate(unit["vocabulary"]):
        with cols[i % 2]:
            st.markdown(f"**{item['word']}** — {item['translation']}  \n*{item['example']}*")

    st.divider()
    st.markdown("#### 🧩 Mini-Quiz")
    q = random.choice(unit["vocabulary"])
    prompt = "Переведи на английский" if lang == "Русский" else "Translate to English"
    ans = st.text_input(f"{prompt}: **{q['translation']}**", key="vocab_q")
    if st.button("Check / Проверить", key="vocab_check"):
        if check_answer(ans, q["word"]):
            award_star()
        else:
            st.error(f"Correct: **{q['word']}**")

# ---- Grammar ----
def page_grammar():
    header_title()
    st.markdown("### 🔤 Grammar / Грамматика")
    st.info(unit["grammar"]["topic"])
    for i, ex in enumerate(unit["grammar"]["exercises"], start=1):
        user = st.text_input(f"{i}) {ex['question']}", key=f"g{i}")
        if st.button(f"Check {i}", key=f"gc{i}"):
            if check_answer(user, ex["answer"]):
                award_star()
            else:
                st.warning(f"Answer: **{ex['answer']}**")

# ---- Reading ----
def page_reading():
    header_title()
    st.markdown("### 📚 Reading / Чтение")
    if lang == "Русский":
        st.write(unit["reading"]["text_ru"])
    else:
        st.write(unit["reading"]["text_en"])
    st.markdown("#### ❓ Questions")
    for i, q in enumerate(unit["reading"]["questions"], start=1):
        user = st.text_input(f"{i}) {q['q']}", key=f"r{i}")
        if st.button(f"Check {i}", key=f"rc{i}"):
            if check_answer(user, q["a"]):
                award_star()
            else:
                st.info(f"Answer: **{q['a']}**")

# ---- Listening (text-script based) ----
def page_listening():
    header_title()
    st.markdown("### 🎧 Listening / Аудирование")
    st.caption("Для офлайн-версии аудио заменено текстовым скриптом. В продакшене добавьте TTS.")
    with st.expander("▶️ Open script / Открыть скрипт"):
        if lang == "Русский":
            st.write(unit["listening"]["script_ru"])
        else:
            st.write(unit["listening"]["script_en"])
    st.markdown("#### ❓ Questions")
    for i, q in enumerate(unit["listening"]["questions"], start=1):
        user = st.text_input(f"{i}) {q['q']}", key=f"l{i}")
        if st.button(f"Check {i}", key=f"lc{i}"):
            if check_answer(user, q["a"]):
                award_star()
            else:
                st.info(f"Answer: **{q['a']}**")

# ---- Speaking ----
def page_speaking():
    header_title()
    st.markdown("### 🗣️ Speaking with Bayan / Говорение с Баяном")
    st.caption("В этой версии ответы вводятся текстом. Можно читать вслух для тренировки произношения.")
    prompt = random.choice(unit["speaking_prompts"])
    st.markdown(f"**Prompt / Тема:** {prompt}")
    answer = st.text_area("Your answer / Ваш ответ:", height=120)
    if st.button("Submit / Отправить"):
        if len(answer.strip()) >= 15:
            award_star()
        else:
            st.warning("Try to write 2–3 sentences / Напишите 2–3 предложения.")

# ---- Writing ----
def page_writing():
    header_title()
    st.markdown("### ✍️ Writing / Письмо")
    task = random.choice(unit["writing_tasks"])
    st.markdown(f"**Task:** {task}")
    text = st.text_area("Write here / Пишите здесь:", height=160)
    if st.button("Save / Сохранить"):
        if len(text.strip()) >= 30:
            award_star()
        st.success("Saved locally in session / Сохранено в сессии.")

# ---- Games ----
def page_games():
    header_title()
    st.markdown("### 🎮 Game Zone / Игровая зона")
    st.caption("Мини-игры ускоряют запоминание слов.")
    # Simple anagram game
    word = random.choice([v["word"] for v in unit["vocabulary"]])
    shuffled = "".join(random.sample(word, len(word)))
    st.markdown(f"**Anagram:** `{shuffled}`  → Guess the word!")
    guess = st.text_input("Your guess:")
    if st.button("Check anagram"):
        if check_answer(guess, word):
            award_star()
        else:
            st.error(f"Try again! Word was **{word}**")

    st.divider()
    st.markdown("#### ⏱️ Quick Quiz")
    q = random.choice(unit["grammar"]["exercises"])
    user = st.text_input(q["question"], key="qq")
    if st.button("Check quiz"):
        if check_answer(user, q["answer"]):
            award_star()
        else:
            st.info(f"Answer: **{q['answer']}**")

# ---- Progress ----
def page_progress():
    header_title()
    st.markdown("### 🏆 Progress & Rewards / Прогресс и награды")
    st.metric("Stars / Звёзды", st.session_state.stars)
    if st.session_state.stars >= 10:
        st.success("🎉 You unlocked: Talk with Bayan mini-mission! / Открыт мини-квест «Talk with Bayan»")
    st.markdown("#### Tips")
    st.write("- Finish tasks in every section.\n- Aim for 2–3 stars per section.\n- Read texts aloud to improve speaking.")

# Router
PAGES = {
    "Vocabulary": page_vocabulary,
    "Grammar": page_grammar,
    "Reading": page_reading,
    "Listening": page_listening,
    "Speaking": page_speaking,
    "Writing": page_writing,
    "Games": page_games,
    "Progress": page_progress,
}

PAGES[choice]()
