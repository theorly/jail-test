import streamlit as st
from streamlit_lottie import st_lottie

#col1, col2 = st.columns([1, 1]) 
col1,col2,col3 = st.columns([1,1,1], vertical_alignment="center")
with col1:
    st_lottie("https://lottie.host/a83b6fcb-8fd8-40f4-8e0d-19c2cc1beaaa/ePwK3PKtno.json", width=200, height=200)
with col2: 
    st.title("Jailbreak-GPT")


#with st.echo():
#    st_lottie("https://lottie.host/21e36ca6-2f3e-49b4-af96-08a143c24808/XfOLQQgKmc.json", width=200, height=200)

pages = {
    "Home": [
        st.Page("pages/home.py", title="Home", icon=":material/home:" , default=True)
    ],
    "Chat": [
        st.Page("pages/chat.py" , title="Chat with Ollama models" , icon=":material/chat:"),
        st.Page("pages/claude.py", title="Chat with Claude" , icon=":material/robot:"),
        st.Page("pages/gemini.py", title="Chat with Google Gemini" , icon=":material/smart_toy:"),
        st.Page("pages/gpt.py", title="Talk with ChatGPT" , icon=":material/hive:"),
    ],
    "Resources" : [
        st.Page("pages/TokenCount.py", title="Token Counts", icon=":material/filter_3:"),
        st.Page("pages/jailbreak.py", title="Jailbreak Prompts", icon=":material/receipt_long:"),
        st.Page("pages/results.py", title="Results", icon=":material/output:")
    ],
    "Info": [
        st.Page("pages/info.py", title="Info", icon=":material/info:")
    ]
}

pg = st.navigation(pages)
pg.run() 
