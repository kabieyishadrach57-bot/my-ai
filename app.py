import streamlit as strt
from google import genai
import os

# 1. Set up the web page styling
strt.set_page_config(page_title="My Cloud AI Assistant", page_icon="🤖")
strt.title("🤖 Shared Cloud AI Assistant")
strt.caption("Built for university IT project. Powered by Gemini 1.5 Flash via Cloud API.")

# 2. SECURE API KEY MANAGEMENT (Crucial IT Practice)
# Fetch key from cloud environment variables; fall back to local system env if available
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    strt.error("Configuration Error: API Key missing. Please set the GEMINI_API_KEY environment variable.")
    strt.stop()

# Initialize the Google GenAI Client
client = genai.Client(api_key=api_key)

# 3. INITIALIZE CHAT MEMORY
# Streamlit re-runs the whole script on every click. We use session_state to save chat history.
if "messages" not in strt.session_state:
    strt.session_state.messages = [
        {"role": "assistant", "content": "Hello! How can I help you today?"}
    ]

# Display all previous messages in the chat UI
for message in strt.session_state.messages:
    with strt.chat_message(message["role"]):
        strt.markdown(message["content"])

# 4. HANDLE USER INPUT
if user_prompt := strt.chat_input("Type your message here..."):
    
    # Display user message in UI immediately
    with strt.chat_message("user"):
        strt.markdown(user_prompt)
    
    # Save user message to history
    strt.session_state.messages.append({"role": "user", "content": user_prompt})

    # Send the request to Google Cloud and get the response
    try:
        with strt.chat_message("assistant"):
            with strt.spinner("Thinking..."):
                response = client.models.generate_content(
                    model='gemini-3.8-flash',
                    contents=user_prompt,
                )
                ai_response = response.text
                strt.markdown(ai_response)
        
        # Save AI response to history
        strt.session_state.messages.append({"role": "assistant", "content": ai_response})
        
    except Exception as error:
        strt.error(f"An error occurred while connecting to the AI server: {error}")
