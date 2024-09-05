import streamlit as st 
from streamlit_option_menu import option_menu
import streamlit as st
import pandas as pd
import numpy as np


st.subheader("Home Page")


selected2 = option_menu(None, ['Option 1', 'Option 2', 'Option 3'], icons = ['🍎', '🍊', '🍇'],menu_icon="cast", default_index = 0, orientation = "horizontal")



df = pd.DataFrame(np.random.randn(50, 20), columns=("col %d" % i for i in range(20)))

st.dataframe(df)  # Same as st.write(df)

