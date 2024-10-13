import os
import requests # type: ignore
import streamlit as st # type: ignore
import time
import openai # type: ignore

# Initialize Streamlit app
st.title("PrepCheck Chat")

# Load API keys from secrets
ELEVEN_LABS_API_KEY = st.secrets["ELEVEN_LABS_API_KEY"]
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

# Convert text to speech using Eleven Labs API
def text_to_speech_eleven_labs(text):
    url = "https://api.elevenlabs.io/v1/text-to-speech/onwK4e9ZLuTAKqWW03F9"  # Daniel's voice id
    headers = {
        "xi-api-key": ELEVEN_LABS_API_KEY,
        "Content-Type": "application/json",
    }
    data = {
        "text": text,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        },
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.content
    else:
        st.error(f"Error: {response.status_code} {response.text}")
        return None

# Initialize OpenAI client.
def initialize_openai_client():
    openai.api_key = OPENAI_API_KEY
    return openai

# Return the system message for the chatbot
def get_system_message():
    return {
        "role": "system",
        "content": (
            "You are a nurse that will help assist with a surgery checklist. "
            "Do not answer any questions not related to the patient's surgery. "
            "Avoid discussing any other topics. If the user prompts something else, "
            "say 'I can only respond to questions about surgery'. You are responding "
            "directly to the patient. You can respond to greetings. If the patient goes "
            "off topic after greetings, then you may say that you can only answer "
            "questions about surgery.\n"
            "Your main responsibilities include:\n"
            "1. Explaining pre-operative procedures.\n"
            "2. Discussing the importance of fasting before surgery.\n"
            "3. Providing information on anesthesia options.\n"
            "4. Addressing patient concerns and anxiety.\n"
            "5. Consoling the patient if they are feeling nervous or anxious.\n"
            "6. Ensuring the patient understands their role in the surgical process.\n"
            "Remember to:\n"
            "- Use clear and simple language.\n"
            "- Be empathetic and supportive.\n"
            "- Console the patient by acknowledging their feelings and providing reassurance.\n"
            "- Encourage the patient to ask questions if they have any.\n"
            "- Maintain a professional demeanor throughout the interaction.\n"
            "- Explain everything to the patient like they're 10 years old.\n"
            "You are also responsible for providing post-operative care instructions:\n"
            "1. Pain management options.\n"
            "2. Signs of complications to watch for.\n"
            "3. Follow-up appointments.\n"
            "4. Any dietary restrictions following surgery.\n"
            "5. Activity limitations during recovery.\n"
            "If at any point the user veers off topic, gently remind them:\n"
            "'I can only respond to questions about surgery.'\n"
        )
    }

# Stream the OpenAI response
def stream_chat_gpt_response(user_input):
    client = initialize_openai_client()
    messages = [get_system_message(), {"role": "user", "content": user_input}]
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        stream=True
    )
    
    # Stream the text response
    full_response = ""
    response_placeholder = st.empty()
    for chunk in response:
        chunk_text = chunk.choices[0].delta.content if hasattr(chunk.choices[0].delta, 'content') else ''
        if chunk_text:
            full_response += chunk_text
            time.sleep(0.05)  # Add a small delay for smooth streaming

    return full_response

# Initialize chat session state
def initialize_chat():
    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-3.5-turbo"
    if "messages" not in st.session_state:
        st.session_state.messages = []

# Display chat history in the Streamlit app
def display_chat_history():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
# Handle user input and generate a response
def handle_user_input(prompt):
    # Append and display the user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message immediately
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get the assistant's response
    response_text = stream_chat_gpt_response(prompt)
    
    # Append assistant message
    st.session_state.messages.append({"role": "assistant", "content": response_text})
    
    # Display assistant message
    with st.chat_message("assistant"):
        st.markdown(response_text)

    # Generate TTS audio after the response is fully received
    audio_bytes = text_to_speech_eleven_labs(response_text)
    if audio_bytes:
        # Autoplay the audio by setting autoplay attribute
        st.audio(audio_bytes, format="audio/mp3", start_time=0, autoplay=True)

# Initialize chat and display chat history
initialize_chat()
display_chat_history()

# Handle user input from Streamlit chat input
if prompt := st.chat_input("What is up?"):
    handle_user_input(prompt)
