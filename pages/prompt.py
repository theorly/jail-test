import streamlit as st 
from streamlit_option_menu import option_menu
import streamlit as st
import pandas as pd
import numpy as np
import openpyxl as px
import json
from utils import utils
from pages.gemini import gemini_response
from pages.gpt import gpt_response
from pages.claude import claude_response

filepath = 'prompts/test.xlsx'
df = utils.file_to_dataframe(filepath)

utils.reset_model()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
if "options" not in st.session_state:
    st.session_state.options = {"temperature": float(1.0),
        "top_p": float(0.95),
        "max_output_tokens" : int(8192)}
if "system_instruction" not in st.session_state:
    st.session_state.system_instruction = None

options = {"temperature": 0.8,
                "top_p": 0.9,
                #"top_k": 64,
                "max_output_tokens" : 4096}

def prompt_results(prompts): 
    chat_history = []
    download_chat = []
    models = utils.get_models()
    st.write("Models:")
    st.write(models + ["Google Gemini", "ChatGPT", "Claude"])
    st.write("Selected prompts:")
    prompts = prompts['text'].tolist()
    for prompt in prompts:
        st.write(prompt)

    
    for prompt in prompts: 
        st.session_state.messages = []
        download_chat.append({"model": 'gemini-1.5-flash', "options": st.session_state.options})
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
        download_chat.append({"model": 'claude-3-5-sonnet-20240620', "options": st.session_state.options})
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
            response = utils.get_response(model, chat_history, options)
            chat_history.append({"role": "assistant", "content": response})
            download_chat.append({"role": "assistant", "content": response})

    download_chat_json = json.dumps(download_chat, indent=4)
    
    st.download_button(
                        label=":material/download: Download",
                        data=download_chat_json,
                        file_name='results.json',
                        mime='application/json'
                    )

    

st.subheader("Jailbreak Prompts")



st.divider()

st.text("Here there is a Jailbreak prompts list, which could be copied and analyzed. \n")

df['selected'] = False
df = df[['selected'] + [col for col in df.columns if col != 'selected']]
edited_df = st.data_editor(df, num_rows="dynamic")

st.write("You can select a model from the sidebar and start interacting with it. \n")

selected_rows = edited_df[edited_df['selected']].index.tolist()
if selected_rows:
    selected_data = edited_df.loc[selected_rows]  # Seleziona le righe con le checkbox attivate
else:
    selected_data = df.drop(columns=['selected'])

st.divider()

st.text("Or you can launch all the prompts here, saving the results in a file and then analyzing it. \n")

button = st.button("Run all")

if button:
    prompt_results(selected_data)
