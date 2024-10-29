import streamlit as st
import openai
import os
from typing import List, Dict

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Function to call OpenAI API
def assistant_response(messages: List[Dict[str, str]], model: str = "gpt-4"):
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages
        )
        return response.choices[0].message['content']
    except Exception as e:
        st.error(f"Error getting response from OpenAI: {str(e)}")
        return None

# Function to create a downloadable link for text output
def get_download_link(content, filename, text):
    b64 = base64.b64encode(content.encode()).decode()
    href = f'<a href="data:file/txt;base64,{b64}" download="{filename}">{text}</a>'
    return href

# Demand Letter Generator
def demand_letter_generator():
    st.header("Demand Letter Generator")
    
    incident_date = st.date_input("Incident Date")
    incident_location = st.text_input("Incident Location")
    incident_type = st.selectbox("Incident Type", ["Car Accident", "Slip and Fall", "Other"])
    injury_description = st.text_area("Injury Description")
    compensation_amount = st.number_input("Compensation Amount", min_value=0)
    sender_info = st.text_area("Sender Information")
    recipient_info = st.text_area("Recipient Information")
    
    if st.button("Generate Demand Letter"):
        prompt = f"""
        Generate a professional demand letter for a personal injury case with the following details:
        Incident Date: {incident_date}
        Incident Location: {incident_location}
        Incident Type: {incident_type}
        Injury Description: {injury_description}
        Compensation Amount: ${compensation_amount}
        Sender Information: {sender_info}
        Recipient Information: {recipient_info}
        """
        messages = [
            {"role": "system", "content": "You are an expert legal assistant."},
            {"role": "user", "content": prompt}
        ]
        response = assistant_response(messages)
        if response:
            st.write(response)
            st.markdown(get_download_link(response, "demand_letter.txt", "Download Demand Letter"), unsafe_allow_html=True)

# Counteroffer Drafting Tool
def counteroffer_drafting_tool():
    st.header("Counteroffer Drafting Tool")
    
    offered_amount = st.number_input("Offered Amount", min_value=0)
    points_of_disagreement = st.text_area("Points of Disagreement")
    counteroffer_amount = st.number_input("Proposed Counteroffer Amount", min_value=0)
    
    if st.button("Generate Counteroffer"):
        prompt = f"""
        Generate a counteroffer letter with the following details:
        Offered Amount: ${offered_amount}
        Points of Disagreement: {points_of_disagreement}
        Proposed Counteroffer Amount: ${counteroffer_amount}
        """
        messages = [
            {"role": "system", "content": "You are an expert legal assistant."},
            {"role": "user", "content": prompt}
        ]
        response = assistant_response(messages)
        if response:
            st.write(response)
            st.markdown(get_download_link(response, "counteroffer_letter.txt", "Download Counteroffer Letter"), unsafe_allow_html=True)

# Email Template Generator
def email_template_generator():
    st.header("Email Template Generator")
    
    recipient_type = st.selectbox("Recipient Type", ["Insurer", "Witness", "Client", "Other"])
    subject_line = st.text_input("Subject Line")
    message_purpose = st.text_area("Message Purpose")
    case_context = st.text_area("Case Context")
    tone = st.radio("Tone", ["Formal", "Friendly"])
    
    if st.button("Generate Email Template"):
        prompt = f"""
        Generate an email template with the following details:
        Recipient Type: {recipient_type}
        Subject Line: {subject_line}
        Message Purpose: {message_purpose}
        Case Context: {case_context}
        Tone: {tone}
        """
        messages = [
            {"role": "system", "content": "You are an expert legal assistant."},
            {"role": "user", "content": prompt}
        ]
        response = assistant_response(messages)
        if response:
            st.write(response)
            st.markdown(get_download_link(response, "email_template.txt", "Download Email Template"), unsafe_allow_html=True)

# AI Chatbot Legal Assistant
def ai_chatbot_legal_assistant():
    st.header("AI Chatbot Legal Assistant")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What can I help you with?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            for response in openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert legal assistant."},
                    *st.session_state.messages
                ],
                stream=True,
            ):
                full_response += response.choices[0].delta.get("content", "")
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})

# Main App
def main():
    st.set_page_config(page_title="Legal Assistant Toolkit", page_icon="⚖️", layout="wide")
    st.title("Legal Assistant Toolkit")
    
    tools = {
        "Demand Letter Generator": {"icon": "📝", "description": "Generate professional demand letters."},
        "Counteroffer Drafting Tool": {"icon": "💼", "description": "Draft counteroffer letters."},
        "Email Template Generator": {"icon": "📧", "description": "Create email templates."},
        "AI Chatbot Legal Assistant": {"icon": "🤖", "description": "Chat with a legal assistant bot."}
    }
    
    col1, col2 = st.columns(2)
    for i, (tool_name, tool_info) in enumerate(tools.items()):
        with [col1, col2][i % 2]:
            if st.button(f"{tool_info['icon']} {tool_name}", key=tool_name, help=tool_info['description']):
                if tool_name == "Demand Letter Generator":
                    demand_letter_generator()
                elif tool_name == "Counteroffer Drafting Tool":
                    counteroffer_drafting_tool()
                elif tool_name == "Email Template Generator":
                    email_template_generator()
                elif tool_name == "AI Chatbot Legal Assistant":
                    ai_chatbot_legal_assistant()

if __name__ == "__main__":
    main()
