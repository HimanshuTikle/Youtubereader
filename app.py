import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai
import os
from youtube_transcript_api import YouTubeTranscriptApi

# Load environment variables
load_dotenv()

# Configure Google Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Set page config
st.set_page_config(page_title="YouTube Summarizer", layout="centered")

# Custom CSS for background and styling
st.markdown("""
    <style>
    body {
        background: linear-gradient(160deg, #0093E9 0%, #80D0C7 100%);
        color: white;
    }
    .header {
        text-align: center;
        padding: 20px;
    }
    .header img {
        width: 100px;
        display: block;
        margin: 0 auto;
    }
    .input-box {
        text-align: center;
        padding: 20px;
    }
    .stButton button {
        background-color: #ff4b4b;
        color: white;
        font-weight: bold;
        border-radius: 10px;
        padding: 10px 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Header with YouTube logo
st.markdown("""
<div class="header">
    <img src="https://upload.wikimedia.org/wikipedia/commons/b/b8/YouTube_Logo_2017.svg" alt="YouTube Logo">
    <h2>YouTube Video Summarizer</h2>
</div>
""", unsafe_allow_html=True)

# Input box for YouTube link
st.markdown('<div class="input-box"><h4>Paste a YouTube Video Link Below:</h4></div>', unsafe_allow_html=True)
youtube_link = st.text_input("Enter YouTube URL here")

# Prompt template
prompt_template = """
Please summarize the following YouTube transcript into 250 words or less, highlighting the key points and main ideas:
"""

# Function to extract transcript
def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("v=")[1].split("&")[0]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = " ".join([t["text"] for t in transcript_text])
        return transcript
    except Exception as e:
        st.error(f"Error fetching transcript: {e}")
        return None

# Function to summarize using Gemini
def generate_gemini_content(transcript_text, prompt):
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt + transcript_text)
        return response.text
    except Exception as e:
        st.error(f"Error generating summary: {e}")
        return None

# Button to generate summary
if st.button("Get Detailed Summary"):
    if youtube_link:
        transcript_text = extract_transcript_details(youtube_link)
        if transcript_text:
            with st.spinner("Summarizing..."):
                summary = generate_gemini_content(transcript_text, prompt_template)
                if summary:
                    st.markdown("## 📝 Summary")
                    st.write(summary)
    else:
        st.warning("Please enter a valid YouTube video link.")
