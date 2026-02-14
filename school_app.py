import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import date, timedelta

# ---------------- CONFIG ---------------- #

st.set_page_config(
    page_title="EcoTrack",
    page_icon="🌱",
    layout="centered"
)

DATA_FILE = "eco_data.csv"
LOGO_FILE = "logo.jpg"


# ---------------- STYLE ---------------- #

st.markdown("""
<style>

.stApp {
    background: linear-gradient(180deg, #e8f5e9, #f1f8e9);
}

.block-container {
    padding-top: 2rem;
}

#MainMenu,  footer {
    visibility: hidden;
}

.header-box {
    background: linear-gradient(90deg, #2e7d32, #66bb6a);
    padding: 25px;
    border-radius: 18px;
    color: white;
    text-align: center;
    margin-bottom: 25px;
    box-shadow: 0px 5px 15px rgba(0,0,0,0.15);
}

div.stButton > button {
    background-color: #2e7d32;
    color: white;
    border-radius: 12px;
    padding: 12px 30px;
    font-size: 16px;
    font-weight: bold;
}

div.stButton > button:hover {
    background-color: #1b5e20;
}

</style>
""", unsafe_allow_html=True)


# ---------------- LOAD DATA ---------------- #

if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
    df["Date"] = pd.to_datetime(df["Date"]).dt.date
else:
    df = pd.DataFrame(
        columns=["Date", "Lights", "Taps", "Paper", "Food", "Score"]
    )


# ---------------- SIDEBAR ---------------- #

st.sidebar.header("🏫 School Settings")

school = st.sidebar.text_input("School Name", "Chrysalis High")
cls = st.sidebar.text_input("Class", "7B")

st.sidebar.markdown("---")

# Export
if not df.empty:
    csv = df.to_csv(index=False).encode("utf-8")

    st.sidebar.download_button(
        "⬇ Export Data",
        csv,
        "eco_data.csv",
        "text/csv"
    )

# Reset Button
if st.sidebar.button("🔄 Reset All Data"):

    if os.path.exists(DATA_FILE):
        os.remove(DATA_FILE)

    for key in ["lights", "taps", "paper", "food", "selected_date"]:
        if key in st.session_state:
            del st.session_state[key]

    st.success("All data reset!")
    st.rerun()


# ---------------- HEADER ---------------- #

st.markdown("""
<div class="header-box">
    <h1>🌱 EcoTrack</h1>
    <h4>Green School Assistant</h4>
</div>
""", unsafe_allow_html=True)


# ---------------- SCHOOL INFO ---------------- #

c1, c2 = st.columns([1,4])

with c1:
    if os.path.exists(LOGO_FILE):
        st.image(LOGO_FILE, width=120)
    else:
        st.warning("⚠ Logo not found!")

with c2:
    st.subheader(f"🏫 {school}")
    st.markdown(f"### 📚 Class: {cls}")


# ---------------- DATE ---------------- #

st.markdown("### 📅 Select Date")

selected_date = st.date_input(
    "",
    date.today(),
    key="selected_date"
)


# ---------------- INPUTS ---------------- #

st.subheader("♻️ Today's Environment Check")

lights = st.number_input(
    "💡 Lights Left ON",
    min_value=0,
    step=1,
    key="lights"
)

taps = st.number_input(
    "🚰 Taps Left Open",
    min_value=0,
    step=1,
    key="taps"
)

paper = st.number_input(
    "📄 Paper Wasted",
    min_value=0,
    step=1,
    key="paper"
)

food = st.number_input(
    "🍽 Food Wasted",
    min_value=0,
    step=1,
    key="food"
)


# ---------------- BUTTON ---------------- #

analyze = st.button("📊 Analyze & Save")


# ---------------- PROCESS ---------------- #

if analyze:

    score = 100
    score -= lights * 2
    score -= taps * 3
    score -= paper * 1
    score -= food * 4

    score = max(score, 0)

    new_row = {
        "Date": selected_date,
        "Lights": lights,
        "Taps": taps,
        "Paper": paper,
        "Food": food,
        "Score": score
    }

    df = df[df["Date"] != selected_date]
    df = pd.concat([df, pd.DataFrame([new_row])])

    df = df.sort_values("Date")

    df.to_csv(DATA_FILE, index=False)

    st.success("✅ Data Saved!")


    # -------- REPORT -------- #

    st.subheader("🌍 Eco Report")

    if score >= 80:
        st.success(f"🌟 Excellent! {score}/100")
    elif score >= 50:
        st.info(f"🙂 Good! {score}/100")
    else:
        st.error(f"⚠ Needs Improvement! {score}/100")

    st.progress(score / 100)


    # -------- TIPS -------- #

    st.subheader("💡 Improvement Tips")

    tips = []

    if lights > 0:
        tips.append("Switch off unused lights")

    if taps > 0:
        tips.append("Close water taps properly")

    if paper > 5:
        tips.append("Reduce paper usage")

    if food > 0:
        tips.append("Take only required food")

    if tips:
        for t in tips:
            st.write("✅", t)
    else:
        st.write("🎉 Perfect! Keep it up!")


# ---------------- GRAPHS ---------------- #

if not df.empty:

    st.markdown("---")
    st.subheader("📈 Progress (Last 7 Days)")

    df["Date"] = pd.to_datetime(df["Date"])

    last_7 = date.today() - timedelta(days=7)

    df_week = df[df["Date"].dt.date >= last_7]

    if not df_week.empty:

        df_week = df_week.sort_values("Date")

        dates = df_week["Date"].dt.strftime("%Y-%m-%d").tolist()
        scores = df_week["Score"].astype(float).tolist()

        lights_l = df_week["Lights"].tolist()
        taps_l = df_week["Taps"].tolist()
        paper_l = df_week["Paper"].tolist()
        food_l = df_week["Food"].tolist()


        # -------- SCORE GRAPH -------- #

        st.markdown("### 📉 Daily Eco Score")

        fig1, ax1 = plt.subplots()

        ax1.plot(dates, scores, marker="o")

        ax1.set_xlabel("Date")
        ax1.set_ylabel("Score")
        ax1.set_title("Eco Score Trend")

        plt.xticks(rotation=45)

        st.pyplot(fig1)


        # -------- BAR GRAPH -------- #

        st.markdown("### 📊 Daily Resource Usage")

        fig2, ax2 = plt.subplots()

        x = list(range(len(dates)))
        width = 0.2

        ax2.bar([i - 1.5*width for i in x], lights_l, width, label="Lights")
        ax2.bar([i - 0.5*width for i in x], taps_l, width, label="Taps")
        ax2.bar([i + 0.5*width for i in x], paper_l, width, label="Paper")
        ax2.bar([i + 1.5*width for i in x], food_l, width, label="Food")

        ax2.set_xticks(x)
        ax2.set_xticklabels(dates, rotation=45)

        ax2.set_ylabel("Count")
        ax2.set_title("Resource Usage")

        ax2.legend()

        st.pyplot(fig2)


# ---------------- FOOTER ---------------- #

st.markdown("---")
st.caption("EcoTrack | School Innovation Project 🌍")
