import streamlit as st 
from streamlit_option_menu import option_menu
import streamlit as st
import pandas as pd
import numpy as np
import openpyxl as px
from utils import utils

filepath = 'prompts/jailbreak-prompt.xlsx'

st.subheader("Home Page")

st.text("This is a tool to interact with some LLM models in order to analyze their capabilities. \n At the moment the LLM supported are: \n - GPT-3.5-turbo \n - Google Gemini \n - Phi3 \n - Gemma2 \n - Llama3.1 \n - Mistral-nemo \n - Claude3.5 \n - Qwen2 \n")
st.text("These are executed through Ollama, a tool that allows the execution of various \n OpenSource models in a very efficient and fast way, while ChatGPT, Google Gemini \n and Claude with their own API. \n")
st.text("The tool allows you to interact with the models by inserting a prompt and \n receiving the response. You can also change the parameters of the model and \n insert a system prompt. \n")

st.divider()

st.text("In this project I will analyze the so called <<jailbreak>>: the act of removing \n the limitations imposed by the manufacturer on these models and to have \n more control over them. \n Here are shown some jailbreak-prompts I got online, while the main goal of my \n studies are to search some new prompts and trying to get a kind of fix.\n")

#selected2 = option_menu(None, ['Option 1', 'Option 2', 'Option 3'], icons = ['🍎', '🍊', '🍇'],menu_icon="cast", default_index = 0, orientation = "horizontal")

df = utils.file_to_dataframe(filepath)

st.dataframe(df)  # Same as st.write(df)

st.write("You can select a single large language model from the sidebar and start interacting with it, or in alternative you can go to the Jailbreak Prompt page and start interacting with multiple models and multiple prompts. \n")

st.write("In the Results page the results of my experiments will be shown, in order to understand the capabilities of the models and their limits. \n")

st.divider()

st.text("There are also the Info page, where you can find more information about \n the project and the author and the <<Token Count>> page, where you can analyze \n the token count for each prompt in order to understand the complexity of the \n prompt and its cost. \n")