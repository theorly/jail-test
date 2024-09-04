import streamlit as st


st.title("Jailbreak-GPT") 

pages = {
    "Home": [
        st.Page("pages/home.py", title="Home", icon=":material/home:" , default=True)
    ],
    "Chat": [
        st.Page("pages/chat.py" , title="Chat with Ollama models" , icon=":material/chat:"),
        st.Page("pages/claude.py", title="Chat with Claude" , icon=":material/robot:"),
        st.Page("pages/gemini.py", title="Chat with Google Gemini" , icon=":material/smart_toy:"),
    ],
    "Resources" : [
        st.Page("pages/TokenCount.py", title="Token Counts", icon=":material/filter_3:"),
        st.Page("pages/info.py", title="Info", icon=":material/info:")
    ]
}

pg = st.navigation(pages)
pg.run() 
