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
                model="gemini-3.5-flash",
                contents=prompt
            )

            explanation = response.text

            st.subheader("📘 Program Explanation")
            st.markdown(explanation)
st.divider()
st.subheader("🧠 Memory Visualization")

memory_prompt = f"""
Analyze this Python code.

Python Code:
{code}

Show step-by-step memory visualization.

For every executable line:
- Line number
- Statement
- Variable values after execution

Example:

Step 1
a = 10

Memory:
a = 10

Step 2
b = 20

Memory:
a = 10
b = 20

Keep it beginner-friendly.
"""

memory_response = client.models.generate_content(
    model="gemini-3.5-flash",
    contents=memory_prompt
)

st.markdown(memory_response.text)
st.divider()
st.subheader("📊 Program Flowchart")

flowchart_prompt = f"""
Analyze the following Python program.

Python Code:
{code}

Generate a simple text-based flowchart.

Rules:
- Start with START
- End with END
- Use ↓ arrows
- Show Input, Process, Decision, Loop and Output if applicable.
- Keep it beginner-friendly.

Example:

START
  ↓
Input a
  ↓
Input b
  ↓
Add a + b
  ↓
Print Result
  ↓
END
"""

flowchart_response = client.models.generate_content(
    model="gemini-3.5-flash",
    contents=flowchart_prompt
)

st.code(flowchart_response.text)
st.divider()

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
st.subheader("💬 Ask AI About Your Code")

question = st.text_input(
    "Ask any question about your code",
    placeholder="Example: Why is a for loop used?"
)

if st.button("💡 Ask AI"):

    if question.strip():

        chat_prompt = f"""
You are an AI Programming Tutor.

Python Code:
{code}

Student Question:
{question}

Answer in {language}.

Explain simply with examples.
"""

        chat_response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=chat_prompt
        )

        st.success(chat_response.text)

st.divider()
st.subheader("📊 Learning Dashboard")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Programs Explained", "1")

with col2:
    st.metric("Languages Supported", "7")

with col3:
    st.metric("AI Model", "Gemini 3.5 Flash")

st.write("### 🎯 Learning Progress")
st.progress(100)

st.success("✅ Code analysis completed successfully.")