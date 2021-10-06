# -*- coding: utf-8 -*-
"""
Created on Sat Oct  2 16:48:14 2021

@author: Amrit
"""

import streamlit as st
import numpy as np
import pandas as pd
#from pages import utils
import matplotlib.pyplot as plt
import seaborn as sns
import os
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.dates as mdates 
xformatter = mdates.DateFormatter('%H:%M') # for time axis plots
#st.set_page_config(page_title='Exploratory Data Analysis of Hourly Solar Data',page_icon=None,layout="wide")

def app():
    if 'main_data.csv' not in os.listdir('data'):
        st.markdown("Please upload data through `Upload Data` page!")
        df=pd.read_csv('data/sample_data.csv')
        df.E_Grid[df.E_Grid.lt(0)] = 0
        df['date'] = pd.to_datetime(df['date'])
        df1 = df.set_index(['date'])
        corrMatrix = df1.corr()
        plt.figure(figsize=(21,7))
        fig_corr = sns.heatmap(corrMatrix,cmap="YlGnBu", annot=True)
        st.pyplot()
        
        fig = px.scatter_matrix(df1,
                                dimensions=["GlobInc", "GlobHor", "T_Amb", "TArray", "EArray", "E_Grid"],
                                color="E_Grid")
        st.plotly_chart(fig)
        

        
    else:
        df=pd.read_csv('data/main_data.csv')
        df.E_Grid[df.E_Grid.lt(0)] = 0
        df['date'] = pd.to_datetime(df['date'])
        df1 = df.set_index(['date'])
        corrMatrix = df1.corr()
        plt.figure(figsize=(21,7))
        fig_corr = sns.heatmap(corrMatrix,cmap="YlGnBu", annot=True)
        st.pyplot()
        
        fig = px.scatter_matrix(df1,
                                dimensions=["GlobInc", "GlobHor", "T_Amb", "TArray", "EArray", "E_Grid"],
                                color="E_Grid")
        fig.update_layout(title="Pair Plot",
                  width=1260,
                  height=720)
        st.plotly_chart(fig)