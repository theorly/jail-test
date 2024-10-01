import anthropic 
import streamlit as st  
import logging
from utils import utils
import os
import json
from dotenv import load_dotenv

load_dotenv()
utils.reset_model()

st.subheader(f"Chat with Claude!")

ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

def claude_response(): 

    message = client.messages.create(
                    model="claude-3-5-sonnet-20240620",
                    temperature= st.session_state.options['temperature'],
                    top_p= st.session_state.options['top_p'],
                    #top_k= st.session_state.options['top_k'],
                    max_tokens= st.session_state.options['max_output_tokens'],
                    messages = st.session_state.messages
            )
    if response.status_code == 200:
        return message.content[0].text
    else:
        st.error("Errore nella risposta di Claude.")
        return ""
    
@st.dialog("Insert a system prompt")
def system_prompt_claude(): 
      with st.container():
            with st.form("system_form"):
                claude_system_prompt = st.text_area("Insert a system prompt")
                submitted = st.form_submit_button("Submit")
                if submitted:
                    st.session_state.messages.append({"role": "system", "content": claude_system_prompt})
                    st.session_state.messages.append({"role": "assistant", "content": claude_response()})
                    logging.debug(f"system prompt: {system_prompt}")
                    logging.debug(f"messages: {st.session_state.messages}")
                    st.rerun()


st.divider()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
# Initialize Claude parameters 
if "options" not in st.session_state:
    st.session_state.options = {"temperature": 0.8,
        "top_p": 0.9,
        "top_k": 64,
        "max_output_tokens" : 4096}

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Insert your prompt!"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            with st.chat_message("assistant"):
                stream = claude_response()
                response = st.write(stream)
            st.session_state.messages.append({"role": "assistant", "content": stream})
        

        # Pulsante per scaricare la cronologia della chat come JSON
chat_history_json = json.dumps(st.session_state.messages, indent=4)


st.divider()
st.divider()
col1, col2, col3, col4 = st.columns([1, 1, 1, 1])  # Due colonne di larghezza uguale
with col1:
    settings = st.button(":material/settings: Settings")  
    if settings:
        utils.change_options()
        st.write("Modifica i parametri del modello")
            
with col2: 
     system_prompt = st.button(":material/point_of_sale: System Prompt") 
     if system_prompt:
                system_prompt_claude()   

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



