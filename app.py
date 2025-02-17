import streamlit as st
import random
from openai import OpenAI
import os
from typing import TypedDict, List, Dict, Any
import requests
from io import BytesIO
from pypdf import PdfReader
import pandas as pd
import plotly.express as px

# --- API Key Management ---
API_KEY = "DeepSeek_API_Key"  # In production, use st.secrets or environment variables

# --- OpenAI Client ---
base_url_deepseek = "https://api.deepseek.com"
try:
    client = OpenAI(api_key=API_KEY, base_url=base_url_deepseek)
except Exception as e:
    st.error(f"Failed to initialize OpenAI client: {e}")
    client = None

# --- Dummy Data Generation ---
def generate_dummy_messages(num_messages=300):
    severity_levels = ["high", "medium", "low"]
    message_types = ["Wildfire", "Earthquake", "Flood"]
    messages = []
    for i in range(num_messages):
        severity = random.choice(severity_levels)
        message_type = random.choice(message_types)
        message = f"Message {i+1}: {message_type} - {severity} severity. Location: {random.choice(['Area A', 'Area B', 'Area C'])}. Details: {random.choice(['Urgent evacuation needed', 'Minor damage reported', 'Alert for potential risk'])}."
        messages.append({"message": message, "severity": severity, "type": message_type})
    return messages

# --- Severity Categorization ---
def categorize_messages(messages):
    high_severity = [msg for msg in messages if msg["severity"] == "high"]
    medium_severity = [msg for msg in messages if msg["severity"] == "medium"]
    low_severity = [msg for msg in messages if msg["severity"] == "low"]
    return high_severity, medium_severity, low_severity

# --- DeepSeek Chat Integration ---
system_prompt = "You are a disaster response agent. Be descriptive and helpful."

def get_deepseek_response(user_prompt, pdf_content):
    if not client:
        return "Error: OpenAI client not initialized"
    
    try:
        combined_prompt = f"{user_prompt}\n\nDocument Content:\n{pdf_content}"
        completion = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": combined_prompt},
            ],
            temperature=0.7,
            max_tokens=350,
        )
        return completion.choices[0].message.content
    except Exception as e:
        st.error(f"Error in DeepSeek API call: {e}")
        return "Sorry, I couldn't process your request at this time."

# --- PDF Processing ---
def read_pdf_from_url(pdf_url):
    try:
        file_id = pdf_url.split('/d/')[1].split('/')[0]
        download_url = f"https://drive.google.com/uc?export=download&id={file_id}"
        response = requests.get(download_url)
        response.raise_for_status()
        pdf_file = BytesIO(response.content)
        pdf_reader = PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        st.error(f"Error processing PDF: {e}")
        return None

# --- Disaster Response Steps ---
def get_disaster_steps(disaster_type):
    steps = {
        "Wildfire": [
            "Evacuate immediately if instructed.",
            "Cover your mouth and nose with a damp cloth.",
            "Stay informed through official channels.",
            "Pack emergency supplies and important documents.",
            "Follow designated evacuation routes."
        ],
        "Earthquake": [
            "Drop, cover, and hold on.",
            "Stay away from windows and exterior walls.",
            "After shaking stops, check for injuries and damage.",
            "Be prepared for aftershocks.",
            "Listen to emergency broadcasts."
        ],
        "Flood": [
            "Move to higher ground immediately.",
            "Avoid walking or driving through floodwaters.",
            "Stay informed about flood warnings and evacuation orders.",
            "Prepare emergency supplies.",
            "Turn off utilities if instructed."
        ],
    }
    return steps.get(disaster_type, ["Steps not available."])

# --- Main Streamlit App ---
def main():
    st.set_page_config(
        page_title="Disaster Management Dashboard",
        page_icon="🚨",
        layout="wide"
    )

    st.title("🚨 Disaster Management Dashboard")
    
    # Initialize session state for dummy messages
    if 'dummy_messages' not in st.session_state:
        st.session_state.dummy_messages = generate_dummy_messages()

    # Sidebar for navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Dashboard", "Chatbot", "Response Guide"])

    if page == "Dashboard":
        st.header("Emergency Messages Overview")
        if st.button("Generate Random Messages"):
            random_messages = random.sample(st.session_state.dummy_messages, 5)
            high, medium, low = categorize_messages(random_messages)

            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📊 Message Distribution")
                severity_counts = {"High": len(high), "Medium": len(medium), "Low": len(low)}
                df = pd.DataFrame(list(severity_counts.items()), columns=['Severity', 'Count'])
                fig = px.bar(df, x='Severity', y='Count', 
                            title='Severity Distribution',
                            color='Severity',
                            color_discrete_map={'High': 'red', 'Medium': 'orange', 'Low': 'green'})
                st.plotly_chart(fig)

            with col2:
                st.subheader("🚨 High Severity Messages")
                for msg in high:
                    st.error(msg["message"])
                
                st.subheader("⚠️ Medium Severity Messages")
                for msg in medium:
                    st.warning(msg["message"])
                
                st.subheader("ℹ️ Low Severity Messages")
                for msg in low:
                    st.info(msg["message"])

    elif page == "Chatbot":
        st.header("💬 Emergency Response Chatbot")
        
        # PDF content (initialized once)
        if 'pdf_content' not in st.session_state:
            pdf_url = "https://drive.google.com/file/d/1Xj2RXKEI120nuY6j-irt_LR1rZTPccoO/view?usp=sharing"
            st.session_state.pdf_content = read_pdf_from_url(pdf_url)

        user_question = st.text_input("Ask a question about disaster management:")
        if user_question:
            if st.session_state.pdf_content:
                with st.spinner("Getting response..."):
                    response = get_deepseek_response(user_question, st.session_state.pdf_content)
                    st.write(response)
            else:
                st.error("PDF content not available. Some features may be limited.")

    elif page == "Response Guide":
        st.header("🆘 Emergency Response Guide")
        
        disaster_type = st.selectbox("Select Disaster Type", ["Wildfire", "Earthquake", "Flood"])
        
        st.subheader(f"Response Steps for {disaster_type}")
        steps = get_disaster_steps(disaster_type)
        
        for i, step in enumerate(steps, 1):
            st.write(f"**{i}.** {step}")
        
        st.info("Remember: Always follow instructions from local authorities and emergency services.")

if __name__ == "__main__":
    main()
