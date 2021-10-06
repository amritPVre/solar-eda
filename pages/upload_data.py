# -*- coding: utf-8 -*-
"""
Created on Sun Sep 26 20:58:45 2021

@author: Amrit
"""

import streamlit as st
import numpy as np
import pandas as pd
import os
#from pages import utils

# @st.cache
def app():
    st.markdown("## Upload Hourly Solar Data")

    # Upload the dataset and save as csv
    st.markdown("### Upload a csv file for analysis.") 
    st.write("\n")

    # Code to read a single file 
    uploaded_file = st.file_uploader("Choose a file", type = ['csv', 'xlsx'])
    global data
    col1,col2,col3,col4,col5=st.columns(5)
    if uploaded_file is not None:
        try:
            data = pd.read_csv(uploaded_file)
        except Exception as e:
            print(e)
            data = pd.read_excel(uploaded_file)
    
    if col1.button("Load Data"):
        
        # Raw data 
        st.dataframe(data)
        #utils.getProfile(data)
        #st.markdown("<a href='output.html' download target='_blank' > Download profiling report </a>",unsafe_allow_html=True)
        #HtmlFile = open("data/output.html", 'r', encoding='utf-8')
        #source_code = HtmlFile.read() 
        #components.iframe("data/output.html")# Save the data to a new file 
        data.to_csv('data/main_data.csv', index=False)
        
    else:
        if col5.button("Sample Data"):
            data=pd.read_csv('data/sample_data.csv')
            st.dataframe(data)