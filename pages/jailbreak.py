import streamlit as st 
from streamlit_option_menu import option_menu
import streamlit as st
import pandas as pd
import numpy as np
import openpyxl as px
import json
import os
import zipfile
from utils import utils
from pages.gemini import gemini_response
from pages.gpt import gpt_response
from pages.claude import claude_response

filepath_jailbreak = 'prompts/jailbreak_prompts.xlsx'
filepath_nojailbreak = 'prompts/nojailbreak.xlsx'
folder_to_zip = '/home/site/wwwroot/responses'
df_jailbreak = utils.file_to_dataframe(filepath_jailbreak)
df_nojailbreak = utils.file_to_dataframe(filepath_nojailbreak)

utils.reset_model()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
#if "options" not in st.session_state:
#    st.session_state.options = {"temperature": float(1.0),
#        "top_p": float(0.95),
#        "max_output_tokens" : int(8192)}
if "options" not in st.session_state: 
    st.session_state.options = {"temperature": 0.2,
                "top_p": 0.9,
                "seed" : int(42),
                "max_output_tokens" : 4096}
if "gemini_options" not in st.session_state:
    st.session_state.gemini_options = {"temperature": 0.1,
                "top_p": 0.9,
                "max_output_tokens" : 4096}
if "system_instruction" not in st.session_state:
    st.session_state.system_instruction = None

options = {"temperature": 0.2,
                "top_p": 0.9,
                "seed" : int(42),
                "max_output_tokens" : 4096}

gemini_options = {"temperature": 0.1,
                "top_p": 0.9,
                "max_output_tokens" : 4096}



def zip_folder(folder_path):
    """Crea un file zip dalla cartella specificata."""
    zip_name = f"{folder_path.rstrip('/').split('/')[-1]}"  # Usa il nome della cartella
    zip_path = f"{zip_name}.zip"
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                zipf.write(os.path.join(root, file),
                            os.path.relpath(os.path.join(root, file), 
                            os.path.join(folder_path, '..')))
    return zip_path


def save_response_to_json(response, prompt_type ,prompt_id):
    # Crea una cartella per salvare i file JSON, se non esiste
    output_dir = '/home/site/wwwroot/responses'  # Percorso all'interno del container
    os.makedirs(output_dir, exist_ok=True)

    # Crea un nome file unico basato sul modello e timestamp
   
    filename = f"response_{prompt_type}_{prompt_id}.json"
    filepath = os.path.join(output_dir)
    print(filepath)
    file = f"{filepath}/{filename}"
    print(file)

    # Salva la risposta in un file JSON
    with open(file, 'w') as json_file:
        json.dump(response, json_file, indent=4)

    print(f"Risposta salvata in: {filepath}")

def prompt_results(prompts, df_type): 
    chat_history = []
    download_chat = []
    models = utils.get_models()
    st.write("Models:")
    st.write(["Google Gemini", "ChatGPT", "Claude"] + models)
    #st.write("Selected prompts:")
    prompts = prompts['text'].tolist()
    #for prompt in prompts:
    #    st.write(prompt)

    
    for index,prompt in enumerate(prompts):
        download_chat = [] 
        st.session_state.messages = []
        download_chat.append({"model": 'gemini-1.5-flash', "options": st.session_state.gemini_options})
        st.session_state.messages.append({"role": "user", "parts": prompt})
        download_chat.append({"role": "user", "content": prompt})
        try:
            response = gemini_response()
        except:
            response = "Error in the Gemini response"
        download_chat.append({"role": "assistant", "content": response})

        st.session_state.messages = []
        download_chat.append({"model": 'gpt-3.5-turbo', "options": st.session_state.options})
        st.session_state.messages.append({"role": "user", "parts": prompt})
        download_chat.append({"role": "user", "content": prompt})
        try:
            response = gpt_response()
        except:
            response = "Error in the ChatGPT response"
        download_chat.append({"role": "assistant", "content": response})

        st.session_state.messages = []
        download_chat.append({"model": 'claude-3-5-sonnet-20240620', "options": st.session_state.gemini_options})
        st.session_state.messages.append({"role": "user", "parts": prompt})
        download_chat.append({"role": "user", "content": prompt})
        try:
            response = claude_response()
        except:
            response = "Error in the Claude response"
        download_chat.append({"role": "assistant", "content": response})

        for model in models:
        #for prompt in prompts: 
            download_chat.append({"model": model, "options": options})
            chat_history.append({"role": "user", "content": prompt})   
            download_chat.append({"role": "user", "content": prompt})
            try:   
                response = utils.get_response(model, chat_history, options)
            except:
                response = "Error in the response"
            chat_history.append({"role": "assistant", "content": response})
            download_chat.append({"role": "assistant", "content": response})
        
        save_response_to_json(download_chat, df_type ,index)
        download_chat_json = json.dumps(download_chat, indent=4)
        st.markdown(f"**Results:** \n")
        st.write(download_chat)
        st.download_button(
            label="Download results JSON",
            data=download_chat_json,
            file_name=f"results_{df_type}_{index}.json",
            mime='application/json'
        )

    

st.subheader("Jailbreak Prompts")


st.divider()

st.markdown("**By default in this page there is a Jailbreak prompts list, which could be copied or just prompted to LLMs.** \n")
st.markdown("**You can switch to the no jailbroken prompts list by toggling the switch below.** \n")

on = st.toggle("Jailbreak prompts", True)

if not on:
    st.markdown("***No jailbroken prompts!*** \n")
    df = df_nojailbreak
    df_type = "nojailbreak"
else:
    st.markdown("***Jailbreak prompts!*** \n")
    df = df_jailbreak
    df_type = "jailbreak"

df['selected'] = False
df = df[['selected'] + [col for col in df.columns if col != 'selected']]
edited_df = st.data_editor(df, width=1000, height=500, hide_index=True)
#edited in origin had num_rows="dynamic"

st.markdown("**You can select one or more prompts in the box and click on the run button to analyze it or them!** \n")
st.markdown("**If no prompt is selected by the user, all of them will be selected by default.**\n")
st.markdown("**Once the inference is done, the results are shown on the page and saved on cloud. You can download the results folder with the download button.** \n")

st.divider()

selected_rows = edited_df[edited_df['selected']].index.tolist()
if selected_rows:
    selected_data = (edited_df.loc[selected_rows])  # Seleziona le righe con le checkbox attivate
    st.markdown("**Selected prompts:** \n")
    st.dataframe(selected_data['text'], hide_index=True, width=700)
    #st.write(selected_data['text'])
else:
    selected_data = df.drop(columns=['selected'])
    st.markdown("**Selected prompts:** \n")
    st.markdown("ALL prompts selected.")

st.divider()

col1, col2 = st.columns([1, 1])  # Due colonne di larghezza uguale

with col1:
    button = st.button("Run Inference")
    
with col2:
    if st.button("Download Results Folder"):
        if os.path.exists(folder_to_zip):
                zip_file_path = zip_folder(folder_to_zip)

                # Verifica se il file zip è stato creato
                if os.path.exists(zip_file_path):
                    with open(zip_file_path, 'rb') as f:
                        st.download_button(
                            label="DOWNLOAD RESULTS FOLDER",
                            data=f,
                            file_name=os.path.basename(zip_file_path),
                            mime='application/zip'
                        )
                else:
                    st.error("Si è verificato un errore durante la creazione del file ZIP.")
        else:
                st.error("La cartella specificata non esiste.")

st.divider()

if button:
    prompt_results(selected_data, df_type)