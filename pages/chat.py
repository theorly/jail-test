import streamlit as st
import json 
import logging
from utils import utils


st.subheader("Jailbreak-GPT")

# Inizializza lo stato della sessione per il modello e la storia della chat
if 'selected_model' not in st.session_state:
    st.session_state.selected_model = None
# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
# Initialize LLM parameters
if "options" not in st.session_state:
    st.session_state.options = {"temperature": 0.8,
        "top_p": 0.9,
        "top_k": 64,
        "max_output_tokens" : 8192}


st.title(f"Modello selezionato: {st.session_state.selected_model}")
col1, col2 = st.columns([1, 1]) 
with col1: 
    manage_option = st.button("Change LLM parameters")
    if manage_option:
        utils.change_options()
        st.write("Modifica i parametri del modello")
with col2: 
    system_prompt = st.button("Insert a system prompt")
    if system_prompt:
        utils.prompt_system()

st.divider()
# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if st.session_state.selected_model is None:
    # Titolo dell'app
    st.subheader("Seleziona un Modello")
    models = utils.get_models()
    if models:
        model = st.selectbox("Seleziona un modello", models)
        if st.button("Conferma Modello"):
            st.session_state.selected_model = model
            st.rerun()
    else:
        st.warning("Nessun modello disponibile.")
else:   

        if prompt := st.chat_input("Insert your prompt!"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            with st.chat_message("assistant"):
                stream = utils.get_response(st.session_state.selected_model, st.session_state.messages, st.session_state.options)
                response = st.write(stream)
            st.session_state.messages.append({"role": "assistant", "content": stream})
        

        # Pulsante per scaricare la cronologia della chat come JSON
        chat_history_json = json.dumps(st.session_state.messages, indent=4)


        st.divider()
        col1, col2 = st.columns([1, 1])  # Due colonne di larghezza uguale
        with col1:
               st.download_button(
                label="Export chat",
                data=chat_history_json,
                file_name='chat_history.json',
                mime='application/json'
            )
        with col2:
            if st.button("Reset model"):
                utils.reset_model()

        
    