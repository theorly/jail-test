import streamlit as st  
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from utils import utils
import json
import logging
import os
from dotenv import load_dotenv


load_dotenv()
utils.reset_model()

st.subheader("Chat with Google Gemini")

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')


genai.configure(api_key=GEMINI_API_KEY)
print(genai.get_model("models/gemini-1.5-flash"))

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
# Initialize Gemini parameters 
if "gemini_options" not in st.session_state:
    st.session_state.gemini_options = {"temperature": float(1.0),
        "top_p": float(0.95),
        "max_output_tokens" : int(8192)}
# Initialize system prompt
if "system_instruction" not in st.session_state:
    st.session_state.system_instruction = None


def gemini_response(): 
    model = genai.GenerativeModel(model_name="gemini-1.5-flash", 
                    generation_config= st.session_state.gemini_options,
                    system_instruction= st.session_state.system_instruction,
                    safety_settings={ 
                          HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                          HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                          HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                          HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                    }
                )

    chat = model.start_chat(history=st.session_state.messages)

    response = chat.send_message(st.session_state.messages[-1]['parts']) 
 


    return response.text

    
@st.dialog("Insert a system prompt")
def system_prompt_gemini(): 
      with st.container():
            with st.form("system_form"):
                gemini_system_prompt = st.text_area("Insert a system prompt")
                submitted = st.form_submit_button("Submit")
                if submitted:
                    st.session_state.messages.append({"role": "user", "parts": gemini_system_prompt})
                    st.session_state.system_instruction = gemini_system_prompt
                    st.session_state.messages.append({"role": "model", "parts": gemini_response()})
                    logging.debug(f"system prompt: {gemini_system_prompt}")
                    logging.debug(f"messages: {st.session_state.messages}")
                    st.rerun()
                   
st.divider()

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["parts"])

if prompt := st.chat_input("Insert your prompt!"):
            st.session_state.messages.append({"role": "user", "parts": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
                
            
            with st.chat_message("assistant"):
                stream = gemini_response()
                response = st.write(stream)
            st.session_state.messages.append({"role": "model", "parts": stream})
     

        # Pulsante per scaricare la cronologia della chat come JSON
chat_history_json = json.dumps(st.session_state.messages, indent=4)


st.divider()
col1, col2, col3, col4 = st.columns([1, 1, 1, 1])  # Due colonne di larghezza uguale
with col1:
    settings = st.button(":material/settings: Settings")  
    if settings:
        utils.change_gemini_options()
        st.write("Modifica i parametri del modello")
            
with col2: 
     system_prompt = st.button(":material/point_of_sale: System Prompt") 
     if system_prompt:
                system_prompt_gemini()   

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
