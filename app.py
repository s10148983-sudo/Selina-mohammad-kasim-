import streamlit as st
from pypdf import PdfReader
from google import genai

# Page Configuration
st.set_page_config(page_title="AI Resume Reasoning System", page_icon="🤖")

st.title("🤖 AI Resume Reasoning System")
st.write("Upload a resume and paste a job description to analyze candidate fit!")

# 1. API Key Input
api_key = st.text_input("Enter your Gemini API Key:", type="password")

# 2. Upload Resume & Job Description
uploaded_file = st.file_uploader("Upload Resume (PDF)", type="pdf")
job_desc = st.text_area("Paste Job Description Here", height=150)

# 3. Process & Analyze
if st.button("Analyze Fit"):
    #Validation checks
    if not api_key:
        st.warning("Please enter your Gemini API Key.")
    elif not uploaded_file:
        st.warning("Please upload a PDF resume.")
    elif not job_desc:
        st.warning("Please paste the job description.")
    else:
        try:
            # Extract text from PDF
            reader = PdfReader(uploaded_file)
            resume_text = ""
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    resume_text += extracted

            # Check if PDF had readable text
            if not resume_text.strip():
                st.error("Could not extract text from this PDF. Please ensure it is not a scanned image.")
                st.stop()

            # Define AI prompt with reasoning instructions
            prompt = f"""
            You are an expert AI HR recruiter. Carefully analyze and evaluate this Resume against the Job Description.

            JOB DESCRIPTION:
            {job_desc}

            RESUME TEXT:
            {resume_text}

            Provide a structured evaluation:
            1. **Match Score**: Overall fit percentage (0% to 100%).
            2. **Key Strengths**: Why the candidate is a good fit.
            3. **Missing Skills / Gaps**: Critical missing qualifications or skills.
            4. **Logical Reasoning**: Step-by-step reasoning explaining why this candidate is or isn't a strong match.
            """

            # Call Gemini AI Model (Using official 'gemini-2.0-flash' model)
            client = genai.Client(api_key=api_key)
            
            with st.spinner("AI is analyzing and reasoning..."):
                response = client.models.generate_content(
                    model="gemini-1.5-flash",
                    contents=prompt,
                )
                
                st.success("Analysis Complete!")
                st.markdown("### 📊 Reasoning & Evaluation Result")
                st.write(response.text)

        except Exception as e:
            st.error(f"Error: {e}")
