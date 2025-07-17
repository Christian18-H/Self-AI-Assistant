import streamlit as st
import google.generativeai as genai
import PyPDF2

# Set up Gemini API key
genai.configure(api_key="AIzaSyDVLjmWaDUyAfgY7RIqFmlUfqObrev5zAk") 

# Initialize Gemini model
model = genai.GenerativeModel("gemini-pro")

# Function to extract text from PDF or TXT file
def extract_text(uploaded_file):
    if uploaded_file.type == "application/pdf":
        try:
            reader = PyPDF2.PdfReader(uploaded_file)
            return "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
        except Exception:
            return None
    elif uploaded_file.type == "text/plain":
        return uploaded_file.read().decode("utf-8")
    return None

# Function to get recommendations from Gemini
def get_recommendation(report_text):
    prompt = f"""
You are a trusted medical AI assistant. Based on the following patient test report, provide:

1. A summary of the key findings,
2. Any noticeable abnormalities or concerns,
3. Professional medical advice or next steps for the patient.

Patient Report:
{report_text}
"""
    response = model.generate_content(prompt)
    return response.text.strip()

# Streamlit UI
st.set_page_config(page_title="Medical AI Assistant", layout="centered")
st.title("🩺 Medical AI Assistant")
st.markdown(
    """
    Upload a patient's medical test report (.pdf or .txt), and this assistant will analyze the content
    and generate a medical summary with recommendations.
    
    **Note:** This tool is for support purposes only. Always verify findings with a licensed doctor.
    """
)

uploaded_file = st.file_uploader("📁 Upload Patient Report", type=["pdf", "txt"])

if uploaded_file:
    with st.spinner("Analyzing the uploaded report..."):
        content = extract_text(uploaded_file)
        if content:
            recommendation = get_recommendation(content)
            st.success("✅ Report Analyzed")
            st.subheader("📝 AI-Generated Medical Summary & Recommendations")
            st.write(recommendation)
        else:
            st.error("❌ Could not read content from the uploaded file. Please try a different format or clear file.")
