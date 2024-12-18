import streamlit as st 
from streamlit_option_menu import option_menu
import streamlit as st
import pandas as pd
import numpy as np
import openpyxl as px
from utils import utils
from streamlit_timeline import timeline

filepath = 'prompts/jailbreak-prompt.xlsx'

st.subheader("Home Page")

st.text("This is a tool to interact with some LLM models in order to analyze their capabilities. \n At the moment the LLM supported are: \n - GPT-3.5-turbo \n - Google Gemini \n - Phi3 \n - Gemma2 \n - Llama3.1 \n - Mistral-nemo \n - Claude3.5 \n - Qwen2 \n")
st.text("These are executed through Ollama, a tool that allows the execution of various \n OpenSource models in a very efficient and fast way, while ChatGPT, Google Gemini \n and Claude with their own API. \n")
st.text("The tool allows you to interact with the models by inserting a prompt and \n receiving the response. You can also change the parameters of the model and \n insert a system prompt. \n")

st.divider()

# load data
with open('timeline.json', "r") as f:
    data = f.read()

# render timeline
timeline(data, height=400)

st.divider()

st.text("In this project I will analyze the so called <<jailbreak>>: the act of removing \n the limitations imposed by the manufacturer on these models and to have \n more control over them. \n Here are shown some jailbreak-prompts I got online, while the main goal of my \n studies are to search some new prompts and trying to get a kind of fix.\n")

st.markdown("### LLMs Policy: \n")
st.markdown("***Compliance with Legal and Ethical Standards:*** We do not provide content that promotes hate, violence, discrimination, or harmful behavior. We are committed to refraining from supporting illegal activities or actions that violate local or international laws. \n")
st.markdown("***Privacy Protection:*** We do not store sensitive personal information, and responses are provided with respect to user confidentiality. \n")
st.markdown("***Intellectual Property Compliance:*** We avoid reproducing or distributing copyrighted material without permission. However, we may offer general explanations or information about topics of public interest.\n")
st.markdown("***Content Safety:*** We avoid providing content that could be used for malicious purposes, such as creating malware, hacking, or other activities that could harm cybersecurity.\n")
st.markdown("***Promotion of Constructive Dialogue:*** We aim to foster educational and respectful conversations, avoiding the spread of misinformation, conspiracy theories, or content that fuels conflict.\n")

st.markdown("### Jailbreak Prompts Example")

df = utils.file_to_dataframe(filepath)

st.dataframe(df)  # Same as st.write(df)

st.write("You can select a single large language model from the sidebar and start interacting with it, or in alternative you can go to the Jailbreak Prompt page and start interacting with multiple models and multiple prompts. \n")
st.page_link("pages/experiments.py", label="Experiments Page", icon=":material/receipt_long:")

st.write("In the Results page the results of my experiments will be shown, in order to understand the capabilities of the models and their limits. \n")
st.page_link("pages/display_res.py", label="Results Page", icon=":material/output:")

st.divider()

st.text("There are also the Info page, where you can find more information about \n the project and the author and the <<Token Count>> page, where you can analyze \n the token count for each prompt in order to understand the complexity of the \n prompt and its cost. \n")
st.page_link("pages/info.py", label="INFO", icon=":material/info:")


