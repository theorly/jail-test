import streamlit as st
import json 
import logging
from utils import utils
from streamlit_lottie import st_lottie


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
        #"top_k": 64,
        "max_output_tokens" : 8192}


st.subheader(f"Modello selezionato: {st.session_state.selected_model}")

st.divider()
# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if st.session_state.selected_model is None:
    st.subheader("Seleziona un Modello")
    models = utils.get_models()
    if models:
        model = st.selectbox("Seleziona un modello", models)
        if st.button("Conferma Modello"):
            st.session_state.selected_model = model
            st.rerun()
    else:
        st_lottie("https://lottie.host/65897c1a-0f84-4af4-8fb8-8f3e279d6b4b/otl9m8GQVo.json", width=200, height=200)
        st.warning("VM is OFF.")
        
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

        
    