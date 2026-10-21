import streamlit as strt
from google import genai
from google.genai import types  # 1. ADDED THIS IMPORT FOR CUSTOMIZATION
import os

# Set up the web page styling
strt.set_page_config(page_title="Falcon AI", page_icon="🦅")
strt.title("🦅 Falcon AI Assistant")
strt.caption("Built for university IT project. Created proudly by Falcon.")

# Secure API key management
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    strt.error("Configuration Error: API Key missing. Please set the GEMINI_API_KEY environment variable.")
    strt.stop()

# Initialize the Google GenAI Client
client = genai.Client(api_key=api_key)

# Initialize chat memory
if "messages" not in strt.session_state:
    strt.session_state.messages = [
        {"role": "assistant", "content": "Hello! I am Falcon. How can I help you today?"}
    ]

# Display all previous messages
for message in strt.session_state.messages:
    with strt.chat_message(message["role"]):
        strt.markdown(message["content"])

# Handle user input
if user_prompt := strt.chat_input("Talk to Falcon..."):
    
    with strt.chat_message("user"):
        strt.markdown(user_prompt)
    
    strt.session_state.messages.append({"role": "user", "content": user_prompt})

    try:
        with strt.chat_message("assistant"):
            with strt.spinner("Falcon is thinking..."):
                
                # 2. ADDED SYSTEM INSTRUCTIONS HERE TO DEFINE THE IDENTITY
                response = client.models.generate_content(
                    model='gemini-2.5-flash',  # Use the model that worked for you
                    contents=user_prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=(
                            "You are Falcon, a highly intelligent and helpful AI assistant. "
                            "You must always remember and openly state that you were created by Falcon, "
                            "a brilliant University IT student. Keep your tone professional, tech-savvy, "
                            "and proud of your creator Falcon."
                        )
                    )
                )
                ai_response = response.text
                strt.markdown(ai_response)
        
        strt.session_state.messages.append({"role": "assistant", "content": ai_response})
        
    except Exception as error:
        strt.error(f"An error occurred while connecting to the AI server: {error}")
