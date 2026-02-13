import streamlit as st

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="EcoTrack - Green School Assistant",
    page_icon="🌱",
    layout="centered"
)

# ---------------- CUSTOM STYLING ---------------- #

st.markdown("""
<style>

/* Background */
.stApp {
    background: linear-gradient(180deg, #e8f5e9, #f1f8e9);
}

/* Add gap at top */
.block-container {
    padding-top: 3rem !important;
}

/* Hide Streamlit default UI */
MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}

/* Remove empty markdown bars */
.stMarkdown:empty {
    display: none !important;
}

/* Header styling */
.header-box {
    background: linear-gradient(90deg, #2e7d32, #66bb6a);
    padding: 25px;
    border-radius: 18px;
    color: white;
    text-align: center;
    margin-bottom: 30px;
    box-shadow: 0px 6px 15px rgba(0,0,0,0.15);
}

/* Button styling */
div.stButton > button {
    background-color: #2e7d32;
    color: white;
    border-radius: 12px;
    padding: 12px 30px;
    border: none;
    font-weight: bold;
    font-size: 16px;
}

div.stButton > button:hover {
    background-color: #1b5e20;
}

</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ---------------- #

st.sidebar.header("🏫 School Settings")

logo = st.sidebar.file_uploader(
    "Upload School Logo",
    type=["png", "jpg", "jpeg"]
)

school_name = st.sidebar.text_input("School Name", "Chrysalis High")
class_name = st.sidebar.text_input("Class", "7B")

# ---------------- HEADER ---------------- #

st.markdown("""
<div class="header-box">
    <h1>🌱 EcoTrack</h1>
    <h4>Green School Assistant</h4>
</div>
""", unsafe_allow_html=True)

# ---------------- SCHOOL INFO ---------------- #

col1, col2 = st.columns([1, 4])

with col1:
    if logo:
        st.image(logo, width=120)

with col2:
    st.subheader(f"🏫 {school_name}")
    st.markdown(f"### 📚 Class: {class_name}")

st.write("")  # small spacing

# ---------------- ENVIRONMENT CHECK ---------------- #

st.subheader("♻️ Today's Environment Check")

lights = st.number_input("💡 Lights Left ON", min_value=0)
water = st.number_input("🚰 Taps Left Open", min_value=0)
paper = st.number_input("📄 Paper Wasted (Sheets)", min_value=0)
food = st.number_input("🍽️ Food Wasted (Plates)", min_value=0)

st.write("")

# ---------------- ANALYZE BUTTON ---------------- #

analyze = st.button("📊 Analyze My Impact")

# ---------------- RESULT ---------------- #

if analyze:

    score = 100
    score -= lights * 2
    score -= water * 3
    score -= paper * 1
    score -= food * 4

    if score < 0:
        score = 0

    st.write("")
    st.subheader("🌍 Eco Report")

    if score >= 80:
        st.success(f"🌟 Excellent! {score}/100")
    elif score >= 50:
        st.info(f"🙂 Good! {score}/100")
    else:
        st.error(f"⚠ Needs Improvement! {score}/100")

    st.progress(score / 100)

    if score >= 90:
        st.balloons()

    st.write("")
    st.subheader("💡 Improvement Tips")

    tips = False

    if lights > 0:
        st.write("✅ Switch off unused lights")
        tips = True

    if water > 0:
        st.write("✅ Close water taps properly")
        tips = True

    if paper > 5:
        st.write("✅ Reduce paper usage")
        tips = True

    if food > 0:
        st.write("✅ Take only required food")
        tips = True

    if not tips:
        st.write("🎉 Perfect! Keep protecting nature!")

    if score >= 80:
        st.success("🌱 Eco Champions! Keep it up!")
    else:
        st.warning("💚 Every small step matters!")

# ---------------- FOOTER ---------------- #

st.markdown("---")
st.caption("EcoTrack | School Innovation Project 🌍")
