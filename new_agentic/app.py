import streamlit as st
from groq import Groq
import os
from dotenv import load_dotenv
import re

# -----------------------------------
# LOAD ENV VARIABLES
# -----------------------------------

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    st.error("GROQ_API_KEY not found. Please add it to your .env file.")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

# -----------------------------------
# STREAMLIT PAGE CONFIG
# -----------------------------------

st.set_page_config(
    page_title="CARE Agent",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 CARE Agent")
st.subheader("Candidate Experience Evaluation System")

st.write(
    "Enter candidate consultation feedback to analyze experience quality using AI."
)

# -----------------------------------
# USER INPUT
# -----------------------------------

feedback = st.text_area(
    "Candidate Feedback",
    height=200,
    placeholder="Example: The consultation was helpful but the HR consultant rushed through my resume and did not clearly explain interview preparation."
)

# -----------------------------------
# AI ANALYSIS FUNCTION
# -----------------------------------

def analyze_feedback(text):

    prompt = f"""
You are an expert HR analytics AI.

Analyze the candidate feedback and provide:

Sentiment
Candidate Experience Score (0-100)
Key Issues Detected
Positive Highlights
HR Improvement Suggestions
AI Reasoning

Feedback:
{text}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are an HR analytics AI system."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    return response.choices[0].message.content

# -----------------------------------
# ANALYZE BUTTON
# -----------------------------------

if st.button("Analyze Experience"):

    if feedback.strip() == "":
        st.warning("Please enter candidate feedback.")
        st.stop()

    with st.spinner("AI analyzing candidate experience..."):

        try:

            result = analyze_feedback(feedback)

            st.success("AI Analysis Complete")

            st.subheader("AI Evaluation Result")
            st.write(result)

            # Try extracting score
            match = re.search(r'(\d{1,3})', result)

            if match:
                score = int(match.group(1))

                if score > 100:
                    score = 100

                st.metric("Candidate Experience Score", f"{score}/100")
                st.progress(score / 100)

        except Exception as e:
            st.error("AI analysis failed.")
            st.write(str(e))

# -----------------------------------
# FOOTER
# -----------------------------------

st.markdown("---")
st.caption("CARE Agent Prototype – AI Powered Candidate Experience Analysis")