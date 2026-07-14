import streamlit as st
from google import genai
import os
from dotenv import load_dotenv
from io import BytesIO

from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

# ------------------------
# Load API Key
# ------------------------
load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("❌ GOOGLE_API_KEY not found in .env file")
    st.stop()

client = genai.Client(api_key=api_key)
st.write("API Key Loaded:", api_key[:10] + "...")

# ------------------------
# Streamlit Page
# ------------------------
st.set_page_config(
    page_title="AI Programming Tutor",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Programming Tutor")
st.write("Paste your Python program and get an AI-powered explanation.")

# ------------------------
# Language Selection
# ------------------------
language = st.selectbox(
    "🌐 Choose Explanation Language",
    [
        "English 🇬🇧",
        "Tamil 🇮🇳",
        "French 🇫🇷",
        "German 🇩🇪",
        "Spanish 🇪🇸",
        "Japanese 🇯🇵",
        "Chinese (Simplified) 🇨🇳"
    ]
)

# ------------------------
# Code Input
# ------------------------
code = st.text_area(
    "💻 Paste your Python Program",
    height=250,
    placeholder="Example:\na=10\nb=20\nprint(a+b)"
)

explain = st.button("🚀 Explain")
if explain:

    if code.strip() == "":
        st.warning("Please paste a Python program.")

    else:

        with st.spinner("Generating explanation..."):

            prompt = f"""
You are an AI Programming Tutor.

Explain the following Python program in {language}.

Python Code:
{code}

Provide:

1. Program Explanation
2. Concepts Used
3. Expected Output
4. Error Detection
5. Execution Flow
6. Code Improvement Suggestions
7. 3 MCQs with Answers
8. Time Complexity
9. Space Complexity

Keep everything beginner-friendly.
"""

            response = client.models.generate_content(
                model="gemini-1.5-flash",
                contents=prompt
            )

            explanation = response.text

            st.subheader("📘 Program Explanation")
            st.markdown(explanation)
                        # ==========================
            # PDF Download
            # ==========================

            buffer = BytesIO()

            doc = SimpleDocTemplate(buffer)
            styles = getSampleStyleSheet()

            story = [
                Paragraph(explanation.replace("\n", "<br/>"), styles["BodyText"])
            ]

            doc.build(story)
            buffer.seek(0)

            st.download_button(
                label="📄 Download Explanation (PDF)",
                data=buffer.getvalue(),
                file_name="program_explanation.pdf",
                mime="application/pdf"
            )

            st.divider()
st.subheader("🧠 Memory Visualization")

memory_prompt = f"""
You are an AI Programming Tutor.

Analyze the following Python code.

Python Code:
{code}

Create a beginner-friendly Memory Visualization.

For every executable line:
1. Show the line number.
2. Show the statement executed.
3. Show the current values of variables.
4. Explain what happened.

Keep the explanation simple.
"""

try:
    memory_response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=memory_prompt
    )

    st.markdown(memory_response.text)

except Exception as e:
    st.warning("⚠️ Unable to generate Memory Visualization at the moment.")
    st.info("The rest of the program analysis is still available.")
    st.divider()
st.subheader("💬 Ask AI About Your Code")

question = st.text_input(
    "Ask any question about your code",
    placeholder="Example: Why is a for loop used?"
)

if st.button("💡 Ask AI"):

    if question.strip() == "":
        st.warning("Please enter a question.")

    else:

        chat_prompt = f"""
You are an AI Programming Tutor.

Python Code:
{code}

Student Question:
{question}

Answer in {language}.

Explain simply with examples.
"""

        try:
            chat_response = client.models.generate_content(
                model="gemini-1.5-flash",
                contents=chat_prompt
            )

            st.success(chat_response.text)

        except Exception:
            st.error("❌ Unable to get AI response right now. Please try again later.")

            st.divider()

st.subheader("📊 Learning Dashboard")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Languages", "7")

with col2:
    st.metric("AI Model", "Gemini")

with col3:
    st.metric("Status", "Active ✅")