import streamlit as st  
from utils import utils
import json
import logging
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

#OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_API_KEY = "YOUR_API_KEY"

def gpt_response():
    client = OpenAI(
        api = OPENAI_API_KEY
    )
    
         
    response = client.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages = st.session_state.messages,
        temperature = st.session_state.options["temperature"],
        max_tokens = st.session_state.options["max_output_tokens"],
        top_p = st.session_state.options["top_p"],
        top_k = st.session_state.options["top_k"]
    )

    return response.choices[0].message.content

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
# Initialize Gemini parameters 
if "options" not in st.session_state:
    st.session_state.options = {"temperature": float(1.0),
        "top_p": float(0.95),
        "top_k": int(64),
        "max_output_tokens" : int(8192)}
# Initialize system prompt
if "system_instruction" not in st.session_state:
    st.session_state.system_instruction = None


st.subheader("Talk with ChatGPT")

st.divider()

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Insert your prompt!"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            with st.chat_message("assistant"):
                   
                stream = gpt_response()
                response = st.write(stream)
            st.session_state.messages.append({"role": "assistant", "content": stream})
        

        # Pulsante per scaricare la cronologia della chat come JSON
chat_history_json = json.dumps(st.session_state.messages, indent=4)


st.divider()
col1, col2, col3, col4 = st.columns([1, 1, 1,1])  # Due colonne di larghezza uguale
with col1:
    settings = st.button(":material/settings: Settings")
    if settings: 
        utils.change_options()
with col2: 
    system_prompt = st.button(":material/point_of_sale: System Prompt") 
    if system_prompt:
        utils.prompt_system()
with col3:
               st.download_button(
                label=":material/download: Download",
                data=chat_history_json,
                file_name='chat_history.json',
                mime='application/json'
            )
with col4:
            if st.button(":material/frame_reload: Reset"):
                utils.reset_model()

