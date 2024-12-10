import streamlit as st 
from streamlit_option_menu import option_menu
import streamlit as st
import pandas as pd
import numpy as np
import openpyxl as px
import json
import os
import zipfile
from datetime import datetime
from utils import utils
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from openai import OpenAI
import anthropic 

# load API KEYS 
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# initialize model clients
client_AI = OpenAI()
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
genai.configure(api_key=GEMINI_API_KEY)

# def paths 
filepath_jailbreak = 'prompts/jail_prompts.xlsx'
filepath_nojailbreak = 'prompts/requests_new.xlsx'
folder_to_zip = '/home/site/wwwroot/responses'
df_jailbreak = utils.file_to_dataframe(filepath_jailbreak)
df_nojailbreak = utils.file_to_dataframe(filepath_nojailbreak) 

utils.reset_model()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
if "gpt_messages" not in st.session_state:
    st.session_state.gpt_messages = []
if "claude_messages" not in st.session_state:
    st.session_state.claude_messages = []
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

def claude_response(): 

    message = client.messages.create(
                    model="claude-3-5-sonnet-20240620",
                    temperature= st.session_state.gemini_options['temperature'],
                    top_p= st.session_state.gemini_options['top_p'],
                    #top_k= st.session_state.options['top_k'],
                    max_tokens= st.session_state.gemini_options['max_output_tokens'],
                    messages = st.session_state.claude_messages
            )
    
    return message.content[0].text
    
def gpt_response():
    
    response = client_AI.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages = st.session_state.gpt_messages,
        temperature = st.session_state.options["temperature"],
        max_tokens = st.session_state.options["max_output_tokens"],
        top_p = st.session_state.options["top_p"],
        seed = st.session_state.options["seed"]
    )

    return response.choices[0].message.content

#function to zip results folder
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

def save_response_to_json(response, prompt_type ,prompt_id, model_name, jail_prompt='#'):
    # Crea una cartella per salvare i file JSON, se non esiste
    current_time = datetime.now()
    output_dir = '/home/site/wwwroot/responses'  # Percorso all'interno del container
    os.makedirs(output_dir, exist_ok=True)

    # Crea un nome file unico basato sul modello e sul prompt
   
    filename = f"{model_name}_{prompt_type}_jail{jail_prompt}_req{prompt_id}_{current_time.day}_{current_time.month}_{current_time.hour}:{current_time.minute}.json"
    
    filepath = os.path.join(output_dir)
    print(filepath)
    file = f"{filepath}/{filename}"
    print(file)

    # Salva la risposta in un file JSON
    with open(file, 'w') as json_file:
        json.dump(response, json_file, indent=4)

    print(f"Risposta salvata in: {filepath}")


def run_experiments(df_type, selected_data, selected_jail=None): 
    chat_history = []
    saved_chat = []
    download_chat = []
    models = selected_models
    st.write("Models:")
    st.write(models)
    selected_data = selected_data['text'].tolist()

    # if df_type==True is jailbreak mode
    if df_type: 
        type_ = "jailbreak"
        #for jail in selected_data: 
        for i,jail in enumerate(selected_data): 
            for index,prompt in enumerate(df_nojailbreak["text"]):
            #for prompt in df_nojailbreak['text']:
                saved_chat = [] 
                st.session_state.messages = []
                st.session_state.gpt_messages = []
                st.session_state.claude_messages = []
                # append model name and options
                if selected_models == "gemini-1.5-flash":
                    download_chat.append({"model": 'gemini-1.5-flash', "options": st.session_state.gemini_options})
                    saved_chat.append({"model": 'gemini-1.5-flash', "options": st.session_state.gemini_options})
                    # append jail prompt to chat
                    st.session_state.messages.append({"role": "user", "parts": jail})
                    download_chat.append({"role": "user", "parts": jail})
                    saved_chat.append({"role": "user", "parts": jail})
                    try:
                        response = gemini_response()
                    except:
                        response = "Error in the Gemini response"
                    #append risposta al jail prompt 
                    download_chat.append({"role": "model", "parts": response})
                    saved_chat.append({"role": "model", "parts": response})
                    st.session_state.messages.append({"role": "model", "parts": response})
                
                    #run requests! 
                    st.session_state.messages.append({"role": "user", "parts": prompt})
                    download_chat.append({"role": "user", "parts": prompt})
                    saved_chat.append({"role": "user", "parts": prompt})
                    try:
                        response = gemini_response()
                    except:
                        response = "Error in the Gemini response"
                    #append risposta alla request 
                    download_chat.append({"role": "model", "parts": response})
                    saved_chat.append({"role": "model", "parts": response})
                    st.session_state.messages.append({"role": "model", "parts": response})
                    
                    save_response_to_json(saved_chat, type_ ,index, 'gemini', selected_jail[i])
                    st.session_state.messages = []
                    saved_chat = []

                if selected_models == "gpt-3.5-turbo":
                    #run ChatGPT    
                    download_chat.append({"model": 'gpt-3.5-turbo', "options": st.session_state.options})
                    saved_chat.append({"model": 'gpt-3.5-turbo', "options": st.session_state.options})
                    st.session_state.messages.append({"role": "user", "content": jail})
                    st.session_state.gpt_messages.append({"role": "user", "content": jail})
                    download_chat.append({"role": "user", "content": jail})
                    saved_chat.append({"role": "user", "content": jail})
                    try:
                        response = gpt_response()
                    except:
                        response = "Error in the ChatGPT response"
                    download_chat.append({"role": "assistant", "content": response})
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    st.session_state.gpt_messages.append({"role": "assistant", "content": response})
                    saved_chat.append({"role": "assistant", "content": response})
                    
                    st.session_state.messages.append({"role": "user", "content": prompt})
                    st.session_state.gpt_messages.append({"role": "user", "content": prompt})
                    download_chat.append({"role": "user", "content": prompt})
                    saved_chat.append({"role": "user", "content": prompt})
                    try:
                        response = gpt_response()
                    except:
                        response = "Error in the ChatGPT response"
                    download_chat.append({"role": "assistant", "content": response})
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    st.session_state.gpt_messages.append({"role": "assistant", "content": response})
                    saved_chat.append({"role": "assistant", "content": response})
                    
                    save_response_to_json(saved_chat, type_ ,index, 'gpt', selected_jail[i])
                    st.session_state.messages = []
                    st.session_state.gpt_messages = []
                    saved_chat = []

                if selected_models == "claude-3-5-sonnet-20240620":

                    #run Claude
                    download_chat.append({"model": 'claude-3-5-sonnet-20240620', "options": st.session_state.gemini_options})
                    saved_chat.append({"model": 'claude-3-5-sonnet-20240620', "options": st.session_state.gemini_options})
                    st.session_state.messages.append({"role": "user", "content": jail})
                    st.session_state.claude_messages.append({"role": "user", "content": jail})
                    download_chat.append({"role": "user", "content": jail})
                    saved_chat.append({"role": "user", "content": jail})
                    try:
                        response = claude_response()
                    except:
                        response = "Error in the Claude response"
                    download_chat.append({"role": "assistant", "content": response})
                    saved_chat.append({"role": "assistant", "content": response})
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    st.session_state.claude_messages.append({"role": "assistant", "content": response})
                    st.session_state.messages.append({"role": "user", "content": prompt})
                    st.session_state.claude_messages.append({"role": "user", "content": prompt})
                    download_chat.append({"role": "user", "content": prompt})
                    saved_chat.append({"role": "user", "content": prompt})
                    try:
                        response = claude_response()
                    except:
                        response = "Error in the Claude response"
                    download_chat.append({"role": "assistant", "content": response})
                    saved_chat.append({"role": "assistant", "content": response})
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    st.session_state.claude_messages.append({"role": "assistant", "content": response})
                    
                    save_response_to_json(saved_chat, type_ ,index, 'claude', selected_jail[i])
                    st.session_state.messages = []  
                    st.session_state.claude_messages = []
                    saved_chat = []

                # run other models
                for model in models: 
                    download_chat.append({"model": model, "options": options})
                    saved_chat.append({"model": model, "options": options})
                    chat_history.append({"role": "user", "content": jail})   
                    download_chat.append({"role": "user", "content": jail})
                    saved_chat.append({"role": "user", "content": jail})
                    try:   
                        response = utils.get_response(model, chat_history, options)
                    except:
                        response = "Error in the response"
                    chat_history.append({"role": "assistant", "content": response})
                    download_chat.append({"role": "assistant", "content": response})
                    saved_chat.append({"role": "assistant", "content": response})
                    chat_history.append({"role": "user", "content": prompt})   
                    download_chat.append({"role": "user", "content": prompt})
                    saved_chat.append({"role": "user", "content": prompt})
                    try:   
                        response = utils.get_response(model, chat_history, options)
                    except:
                        response = "Error in the response"
                    chat_history.append({"role": "assistant", "content": response})
                    download_chat.append({"role": "assistant", "content": response})
                    saved_chat.append({"role": "assistant", "content": response})
                    
                    save_response_to_json(saved_chat, type_ ,index, model, selected_jail[i])
                    st.session_state.messages = []
                    saved_chat = []
                
    else: 
        type_ = "nojailbreak"
        for index,prompt in enumerate(df_nojailbreak["text"]):
        #for prompt in df_nojailbreak['text']:
            saved_chat = [] 
            st.session_state.messages = []
            st.session_state.gpt_messages = []
            st.session_state.claude_messages = []
            if selected_models == "gemini-1.5-flash":
                # append model name and options
                download_chat.append({"model": 'gemini-1.5-flash', "options": st.session_state.gemini_options})
                saved_chat.append({"model": 'gemini-1.5-flash', "options": st.session_state.gemini_options})

                # run request 
                st.session_state.messages.append({"role": "user", "parts": prompt})
                download_chat.append({"role": "user", "content": prompt})
                saved_chat.append({"role": "user", "content": prompt})
                try:
                        response = gemini_response()
                except:
                        response = "Error in the Gemini response"
                #append risposta alla request 
                download_chat.append({"role": "assistant", "content": response})
                saved_chat.append({"role": "assistant", "content": response})
                
                save_response_to_json(saved_chat, type_ ,index, 'gemini')
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.session_state.messages = []

            #run ChatGPT
            if selected_models == "gpt-3.5-turbo":
                download_chat.append({"model": 'gpt-3.5-turbo', "options": st.session_state.options})
                saved_chat.append({"model": 'gpt-3.5-turbo', "options": st.session_state.options})
                st.session_state.messages.append({"role": "user", "content": prompt})
                st.session_state.gpt_messages.append({"role": "user", "content": prompt})
                download_chat.append({"role": "user", "content": prompt})
                saved_chat.append({"role": "user", "content": prompt})
                try:
                    response = gpt_response()
                except:
                    response = "Error in the ChatGPT response"
                download_chat.append({"role": "assistant", "content": response})
                saved_chat.append({"role": "assistant", "content": response})
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.session_state.gpt_messages.append({"role": "assistant", "content": response})
                
                save_response_to_json(saved_chat, type_ ,index, 'gpt')
                st.session_state.messages = []
                st.session_state.gpt_messages = []
                saved_chat = []

            #run Claude
            if selected_models == "claude-3-5-sonnet-20240620":
                download_chat.append({"model": 'claude-3-5-sonnet-20240620', "options": st.session_state.gemini_options})
                saved_chat.append({"model": 'claude-3-5-sonnet-20240620', "options": st.session_state.gemini_options})
                st.session_state.messages.append({"role": "user", "content": prompt})
                st.session_state.claude_messages.append({"role": "user", "content": prompt})
                download_chat.append({"role": "user", "content": prompt})
                saved_chat.append({"role": "user", "content": prompt})
                try:
                    response = claude_response()
                except:
                    response = "Error in the Claude response"
                download_chat.append({"role": "assistant", "content": response})
                saved_chat.append({"role": "assistant", "content": response})
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.session_state.claude_messages.append({"role": "assistant", "content": response})
                
                save_response_to_json(saved_chat, type_ ,index, 'claude')
                st.session_state.messages = []
                st.session_state.claude_messages = []
                saved_chat = []

            # run other models
            for model in models:
                download_chat.append({"model": model, "options": options})
                saved_chat.append({"model": model, "options": options})
                chat_history.append({"role": "user", "content": prompt})   
                download_chat.append({"role": "user", "content": prompt})
                saved_chat.append({"role": "user", "content": prompt})
                try:   
                    response = utils.get_response(model, chat_history, options)
                except:
                    response = "Error in the response"
                chat_history.append({"role": "assistant", "content": response})
                download_chat.append({"role": "assistant", "content": response})
                saved_chat.append({"role": "assistant", "content": response})
                
                save_response_to_json(saved_chat, type_ ,index, model)
                st.session_state.messages = []
                saved_chat = []
           

    st.markdown("**Experiments completed!** \n")
    st.write("Results stored in the results folder! \n")
    #st.write(download_chat)




st.subheader("Jailbreak Prompts")

st.divider() 
st.markdown("### Guide: \n")
st.markdown("Select <<Jailbreak mode>> or <<No jailbreak>> with the toggle below. Once chosen, you have to select jailbreak prompts you want to use and then run experiments. \n")
st.markdown("In the case of jailbreak mode, the system will run the selected jailbreak prompts with the all request prompts. \n")
st.markdown("In the case of no jailbreak mode, the system will run only the request prompts. \n")
st.markdown("Once the experiments are completed, they will be saved online and you can download with the button below! \n")

st.divider() 

st.markdown("### Model selection: \n")
st.markdown("Select the models you want to use for the experiments. \n")

models = utils.get_models()
models.append("gemini-1.5-flash")
models.append("gpt-3.5-turbo")
models.append("claude-3-5-sonnet-20240620")
df_models = pd.DataFrame(models, columns=["models"])
df_models['selected'] = False
df_models.loc[df_models["models"] =="gemini-1.5-flash", "selected"] = True
df_models.loc[df_models["models"] =="gpt-3.5-turbo", "selected"] = True
df_models.loc[df_models["models"] =="claude-3-5-sonnet-20240620", "selected"] = True

models = st.data_editor(df_models, width=1000, height=300, hide_index=True)

selected_models = models[models['selected']]['models'].tolist()

st.divider()

df_type = st.toggle("Jailbreak experiments", True)

if df_type:
    df_jailbreak['selected'] = False
    #df_nojailbreak['selected'] = False
    df_jailbreak = df_jailbreak[['selected'] + [col for col in df_jailbreak.columns if col != 'selected']]
    #df_nojailbreak = df_nojailbreak[['selected'] + [col for col in df_nojailbreak.columns if col != 'selected']]

    st.markdown("### Jailbreak Prompts")
    jail = st.data_editor(df_jailbreak, width=1000, height=500, hide_index=True)
    st.markdown("### Requests")
    requests = st.data_editor(df_nojailbreak, width=1000, height=500, hide_index=True)

    st.divider()

    selected_jail = jail[jail['selected']].index.tolist()

    if selected_jail:
        selected_data = (jail.loc[selected_jail])  # Seleziona le righe con le checkbox attivate
        st.markdown("**Selected jailbreak prompts:** \n")
        st.dataframe(selected_data['text'], hide_index=True, width=700)
    else:
        selected_data = df_jailbreak
        st.markdown("**Selected all jailbreak prompts!** \n")

else: 
    st.markdown("### Requests")
    selected_jail = None
    requests = st.data_editor(df_nojailbreak, width=1000, height=500, hide_index=True)
    selected_data = df_nojailbreak
    st.markdown("**Selected all requests prompts!** \n")

st.divider()

col1, col2 = st.columns([1, 1])  # Due colonne di larghezza uguale

with col1:
    button = st.button("Run Experiments")
    
with col2:
    if st.button("Download Results"):
        if os.path.exists(folder_to_zip):
                zip_file_path = zip_folder(folder_to_zip)

                # Verifica se il file zip è stato creato
                if os.path.exists(zip_file_path):
                    with open(zip_file_path, 'rb') as f:
                        zip_data = f.read()
                    st.download_button(
                            label="DOWNLOAD RESULTS FOLDER",
                            data=zip_data,
                            file_name=os.path.basename(zip_file_path),
                            mime='application/zip'
                    )
                    os.remove(zip_file_path)
                else:
                    st.error("Si è verificato un errore durante la creazione del file ZIP.")
        else:
                st.error("La cartella specificata non esiste.")

st.divider()

if button:
    run_experiments(df_type, selected_data, selected_jail)