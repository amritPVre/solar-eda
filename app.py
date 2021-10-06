# -*- coding: utf-8 -*-
"""
Created on Sun Sep 26 20:44:40 2021

@author: Amrit
"""

import os
import streamlit as st
import numpy as np
from PIL import  Image

# Custom imports 
from MultiPage import MultiPage
from pages import upload_data, hourly_data, EDA #machine_learning, metadata, data_visualize, redundant # import your pages here

# Create an instance of the app 
app = MultiPage()

st.set_page_config(page_icon=None,layout="wide")

# Title of the main page
display = Image.open('Logo.png')
display = np.array(display)
# st.image(display, width = 400)
# st.title("Data Storyteller Application")
col1, col2 = st.columns(2)
col1.image(display, width = 400)
col2.title("Hourly Solar Data Analytics App")

# Add all your application here
app.add_page("Upload Data", upload_data.app)
app.add_page("Hourly Data", hourly_data.app)
app.add_page("Exploratory Data Analysis", EDA.app)
#app.add_page("Data Analysis",data_visualize.app)
#app.add_page("Y-Parameter Optimization",redundant.app)

# The main app
app.run()
