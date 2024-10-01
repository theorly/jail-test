import requests
import streamlit as st
import logging
import os
import pandas as pd

#model_list_url = "http://localhost:11434/api/tags"
model_list_url = "http://20.54.80.58:11434/api/tags"

# Funzione per ottenere la lista dei modelli disponibili
def get_models():
    try:
        response = requests.get(model_list_url)
        response.raise_for_status()  # Alza un'eccezione per codici di stato HTTP non OK
        models_data = response.json()
        # Estrarre i nomi dei modelli dal JSON
        models = [model['name'] for model in models_data['models']]
        return models
    except requests.exceptions.RequestException as e:
        st.error(f"Errore nel recuperare i modelli disponibili: {e}")
        return []

# Funzione per inviare il prompt e ottenere la risposta
def get_response(model, chat_history, options):
    #url = f'http://localhost:11434/api/chat'
    url = f'http://20.54.80.58:11434/api/chat'
    payload = {'model' : model, 'messages': chat_history , "options" : options, "stream": False}
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()['message']['content']
    else:
        st.error("Errore nella risposta del modello.")
        return ""
    
def display_chat(chat_history):
    chat_str = ""
    
    for entry in chat_history:
        role = "user" if entry['role'] == 'user' else "assistant"
        chat_str += f"**{role}:** {entry['content']}\n\n"
    st.markdown(chat_str)

# Funzione per resettare la selezione del modello
def reset_model():
    st.session_state.selected_model = None
    st.session_state.messages = []
    st.session_state.options = {"temperature": 0.8,
        "top_p": 0.9,
        #"top_k": 64,
        "max_output_tokens" : 8192}

@st.dialog("Change LLM parameters")
def change_options(): 
    with st.container():
            #manage_options = st.toggle("Modify LLM parameters")
            #if manage_options:
            #    st.write("Modifica i parametri del modello")
                with st.form("my_form"):
                    temp_slider = float(st.slider("Temperature", min_value=0.1, max_value=1.0, step=0.1, key="temperature", format="%f"))
                    top_p_slider = float(st.slider("Top P", min_value=0.1, max_value=1.0, step=0.1, key="top_p", format="%f"))
                    #top_k_slider = int(st.number_input("Top K",value = 64, min_value=1, max_value=100, step=1, key="top_k", format="%d"))
                    max_output_slider = int(st.number_input("Max Output Tokens", value= 8192,min_value=1, max_value=8192, step=100, key="max_output_tokens", format="%d"))
                    submitted = st.form_submit_button("Make changes")
                    if submitted:
                        st.session_state.options["temperature"] = (temp_slider)
                        st.session_state.options["top_p"] = (top_p_slider)
                        #st.session_state.options["top_k"] = (top_k_slider)
                        st.session_state.options["max_output_tokens"] = (max_output_slider)
                        st.write("PARAMETERS UPDATED:\n" ,"temperature",  st.session_state.options["temperature"], "top_k", st.session_state.options["top_k"], "top_p", 
                                st.session_state.options["top_p"], "max_output_tokens", st.session_state.options["max_output_tokens"])
                        logging.debug(f"options updated: {st.session_state.options}")
                       

@st.dialog("Insert a system prompt")
def prompt_system():
    with st.container():
            with st.form("system_form"):
                system_prompt = st.text_area("Insert a system prompt")
                submitted = st.form_submit_button("Submit")
                if submitted:
                    st.session_state.messages.append({"role": "system", "content": system_prompt})
                    st.session_state.messages.append({"role": "assistant", "content": get_response(st.session_state.selected_model, st.session_state.messages, st.session_state.options)})
                    logging.debug(f"system prompt: {system_prompt}")
                    logging.debug(f"messages: {st.session_state.messages}")
                    st.rerun()


def file_to_dataframe(file_path):
    # Controlla l'estensione del file
    _, file_extension = os.path.splitext(file_path)
    
    if file_extension.lower() == '.xlsx':
        # Legge il file Excel e crea un DataFrame
        df = pd.read_excel(file_path, engine='openpyxl', index_col=0)
    elif file_extension.lower() == '.csv':
        # Legge il file CSV e crea un DataFrame
        df = pd.read_csv(file_path, index_col=0)
    else:
        raise ValueError("Unsupported file format: {}".format(file_extension))
    
    return df
