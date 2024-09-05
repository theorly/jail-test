import streamlit as st 
from streamlit_card import card 
from streamlit_option_menu import option_menu
import streamlit as st
import pandas as pd
import numpy as np


st.subheader("Home Page")


hasClicked = card(
    title = "Click me",
    text = "Click me to see the magic", 
    image = "https://media.giphy.com/media/3o7TKz9bX9v6hZ8NSA/giphy.gif"
)

selected2 = option_menu(None, ['Option 1', 'Option 2', 'Option 3'], icons = ['🍎', '🍊', '🍇'],menu_icon="cast", default_index = 0, orientation = "horizontal")



df = pd.DataFrame(np.random.randn(50, 20), columns=("col %d" % i for i in range(20)))

st.dataframe(df)  # Same as st.write(df)

