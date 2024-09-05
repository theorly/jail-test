import streamlit as st
from transformers import GPT2Tokenizer

class TokenCalculator:
    def __init__(self, model_name='gpt2'):
        self.tokenizer = GPT2Tokenizer.from_pretrained(model_name)

    def count_tokens(self, text):
        tokens = self.tokenizer.encode(text)
        return len(tokens)
    
def get_token(text):
    calculator = TokenCalculator()
    return calculator.count_tokens(text)

st.subheader("Token Count")

text = st.text_area("Insert your prompt here")
button = st.button("Count Tokens")

if button:
    token_count = get_token(text)
    st.write(f"Number of Token: {token_count}")

