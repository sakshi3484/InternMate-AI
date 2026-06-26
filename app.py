import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from pypdf import PdfReader

# Load API key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("API Key not found! Please check your .env file.")
    st.stop()

# Configure Gemini
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.5-flash")

# ---------------- UI ----------------
st.title("🤖 InternMate AI")
st.subheader("Your Internship Preparation Agent")

# ---------------- Student Profile ----------------
st.header("Student Profile")

name = st.text_input("Your Name")
education = st.text_input("Your Degree / Branch")
skills = st.text_area("Your Current Skills", placeholder="Python, ML, SQL, Streamlit")
goal = st.text_input("Target Internship Role")

# ---------------- Resume Upload ----------------
st.header("Upload Resume (Optional) 📄")

resume_text = ""

resume = st.file_uploader("Upload your resume PDF", type=["pdf"])

if resume is not None:
    pdf_reader = PdfReader(resume)
    for page in pdf_reader.pages:
        text = page.extract_text()
        if text:
            resume_text += text
            
            

# ---------------- Option Selection ----------------
st.header("What do you need help with?")

option = st.selectbox(
    "Choose:",
    [
        "Internship Roadmap",
        "Resume Guidance",
        "Interview Preparation",
        "Project Ideas",
        "Skill Gap Analysis"
    ]
)

# ---------------- Generate Button ----------------
if st.button("Generate Plan 🚀"):

    if not name or not skills or not goal:
        st.warning("Please fill in at least Name, Skills, and Target Role.")
        st.stop()

    prompt = f"""
You are InternMate AI, a highly skilled internship preparation mentor.

Student Details:
Name: {name}
Education: {education}
Skills: {skills}
Target Role: {goal}

Resume Content:
{resume_text}

Task:
{option}

Give practical, structured, beginner-friendly guidance.
Use headings and bullet points.
"""



    try:
        response = model.generate_content(prompt)

        if response and response.candidates:
            st.success("Your Personalized Guidance")
            st.write(response.text)
        else:
            st.error("Gemini returned no response.")

    except Exception as e:
        st.error(f"Gemini Error: {e}")