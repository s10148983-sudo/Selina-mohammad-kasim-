import streamlit as st
import google.generativeai as genai
import pypdf
import io

# 1. Page Configuration
st.set_page_config(page_title="AI Resume Reasoning System", page_icon="🤖")

st.title("🤖 AI Resume Reasoning System")
st.write("Upload a resume and paste a job description to analyze candidate fit!")

# 2. API Key Input Box
api_key = st.text_input("Enter your Gemini API Key:", type="password")

# 3. Resume File Uploader & Job Description Input
uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
job_description = st.text_area("Paste Job Description Here", height=150)

# Helper function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    pdf_reader = pypdf.PdfReader(io.BytesIO(pdf_file.read()))
    text = ""
    for page in pdf_reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"
    return text

# 4. Analyze Button Click Event
if st.button("Analyze Fit"):
    # Validation checks
    if not api_key:
        st.error("Please enter a valid Gemini API Key!")
    elif not uploaded_file:
        st.error("Please upload a PDF resume!")
    elif not job_description.strip():
        st.error("Please enter the Job Description!")
    else:
        try:
            # Configure Gemini API dynamically with user provided key
            genai.configure(api_key=api_key.strip())
            
            # Using latest active model: gemini-2.0-flash
            model = genai.GenerativeModel("gemini-2.0-flash")

            with st.spinner("Analyzing Candidate Fit... Please wait!"):
                # Extract PDF text
                resume_text = extract_text_from_pdf(uploaded_file)

                # Prompt construction
                prompt = f"""
                You are an expert HR and Talent Acquisition Specialist.
                Analyze the following candidate's resume against the provided Job Description.

                ### Job Description:
                {job_description}

                ### Resume Content:
                {resume_text}

                ### Tasks:
                1. Provide a Match Percentage (0% to 100%).
                2. Key Strengths / Matching Skills.
                3. Missing Skills / Gaps.
                4. Final Recommendation (Shortlisted / Rejected / Needs Further Assessment).
                """

                # Call Gemini API
                response = model.generate_content(prompt)

                # Display Output
                st.success("Analysis Complete!")
                st.markdown("### 📊 Analysis Results")
                st.write(response.text)

        except Exception as e:
            st.error(f"Error: {e}")
            
