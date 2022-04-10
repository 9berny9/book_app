import pandas as pd
import numpy as np
import streamlit as st

#
st.write("""
# bookREC
Find friends for your book!
""")
book = st.text_input('Type the title and press Enter')