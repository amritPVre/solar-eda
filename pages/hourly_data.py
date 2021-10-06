# -*- coding: utf-8 -*-
"""
Created on Sun Sep 26 22:08:19 2021

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
st.set_option('deprecation.showPyplotGlobalUse', False)


def app():
    if 'main_data.csv' not in os.listdir('data'):
        st.markdown("Please upload data through `Upload Data` page!")
        df=pd.read_csv('data/sample_data.csv')
        df.E_Grid[df.E_Grid.lt(0)] = 0
        df['date'] = pd.to_datetime(df['date'])
        df1 = df.set_index(['date'])
        
        #Metrics-Backend
        df1_sum=df1.sum(axis=0, skipna=True)
        dfd=df[df["E_Grid"] != 0.0].resample('D', on='date').mean()
        Tmod=dfd.TArray.mean()
        dfTamb=df.resample('Y', on='date').mean()
        
        
        #Metrics-Frontend
        col1,col2,col3,col4,col5=st.columns(5)
        col1.metric(label="Total GHI (kWh/m\u00b2/year)", value="{:.2f}".format(df1_sum.GlobHor/1000))
        col2.metric(label="Total GII (kWh/m\u00b2/year)", value="{:.2f}".format(df1_sum.GlobInc/1000))
        col3.metric(label="Annual PR (%)", value="{:.0%}".format(df1_sum.E_Grid*1000/df1_sum.GlobInc/12000))
        col4.metric(label="Yearly Energy Yield (MWh/year)", value="{:.2f}".format(df1_sum.E_Grid/1000))
        col5.metric(label="Yearly Avg PV Temperature (\u00b0C)", value="{:.2f}".format(Tmod))
        
        st.markdown("----------------------------------------")
        
        cols1,cols2,cols4,cols5=st.columns(4)
        cols1.metric(label="Peak GHI(W/m\u00b2)",value="{:.2f}".format(df1.GlobHor.max()))
        cols2.metric(label="Peak GII(W/m\u00b2)",value="{:.2f}".format(df1.GlobInc.max()))
        #cols3.markdown(" ")
        cols4.metric(label="Ambient Temperature(\u00b0C)",value="Max: "+str(float("{:.1f}".format(df1.T_Amb.max())))+"\u00b0C",delta = "Min: "+str(float(df1.T_Amb.min()))+"\u00b0C", delta_color = 'inverse')
        cols5.metric(label="Module Temperature(\u00b0C)",value = "Max: "+str(float("{:.2f}".format(df1.TArray.max())))+"\u00b0C", delta = "Min: "+str(float("{:.2f}".format(df1.TArray.min())))+"\u00b0C", delta_color = 'inverse')
        
        #st.info('Info message')

        

        
        col1,col2=st.columns(2)
        #Irradiance Graph
        fig1 = px.line(df1, y=["GlobInc", "GlobHor"],title='Hourly Solar Irradiance (W/m\u00b2) GII & GHI',width=620,height=460)
        fig1.update_layout(title_text='<b>Hourly Solar Irradiance (W/m\u00b2) GII & GHI</b>', title_x=0.5,
                   xaxis_title="Time (in HH:MM)",yaxis_title="Irradiance (W/m\u00b2)")
        col1.plotly_chart(fig1)
        
        #Temperature Graph
        fig2 = px.line(df1, y=["TArray", "T_Amb"],title='Hourly Temperature Distribution (W/m\u00b2) Ambient & Module Temperature',width=620,height=460)
        fig2.update_layout(title_text='<b>Hourly Temperature Distribution (W/m\u00b2) Ambient & Module Temperature</b>', title_x=0.5,
                   xaxis_title="Time",yaxis_title="Temperature (\u00b0C)")
        col2.plotly_chart(fig2)
        
        col1,col2=st.columns(2)
        col1.info('Info message')
        col2.info('Info message')
        
        st.markdown("----------------------------------------")
        
        cols1,cols2,cols4,cols5=st.columns(4)
        cols1.metric(label="Max DC Power(kW)",value="{:.2f}".format(df1.EArray.max()))
        cols2.metric(label="Max AC Power(kW)",value="{:.2f}".format(df1.E_Grid.max()))
        #cols3.markdown(" ")
        cols4.metric(label="Yearly Avg GII(kWh/m\u00b2/day)",value="{:.2f}".format(df1_sum.GlobInc.mean()/1000))
        cols5.metric(label="Yearly Avg Amb Temperature(\u00b0C)",value ="{:.2f}".format(dfTamb.T_Amb.max())+"\u00b0C")
        
        
        
        colx,coly=st.columns(2)
        #E_Grid & EArray Graph
        figx = px.line(df1, y=["EArray", "E_Grid"],title='Hourly DC & AC Power(kW) Generation Over the Year',width=620,height=460)
        figx.update_layout(title_text='<b>Hourly DC & AC Power(kW) Generation Over the Year</b>', title_x=0.5,
                   xaxis_title="Time",yaxis_title="Power (kW)")
        colx.plotly_chart(figx)
        
        #E_Grid Vs GII Graph
        figy = px.scatter(df1,x="GlobInc", y="E_Grid",title='Hourly AC Power(kW) Vs GII (W/m\u00b2) Plot',width=620,height=460,color='TArray')
        figy.update_layout(title_text='<b>Hourly AC Power(kW) Vs GII (W/m\u00b2) Plot</b>', title_x=0.5,
                   xaxis_title="GII (W/m\u00b2)",yaxis_title="E_Grid (kW)")
        coly.plotly_chart(figy)
 
    
        df3x=df1
        df3x['date'] = df3x.index
        # adding separate time and date columns
        df3x["DATE"] = pd.to_datetime(df3x['date']).dt.date # add new column with date
        df3x["TIME"] = pd.to_datetime(df3x['date']).dt.time # add new column with time
        # add hours and minutes for ml models
        df3x['HOURS'] = pd.to_datetime(df3x['TIME'],format='%H:%M:%S').dt.hour
        df3x['MINUTES'] = pd.to_datetime(df3x['TIME'],format='%H:%M:%S').dt.minute
        df3x['MINUTES_PASS'] = df3x['MINUTES'] + df3x['HOURS']*60

        # add date as string column
        colDC, colAC=st.columns(2)
        df3x["DATE_STR"] = df3x["DATE"].astype(str) # add column with date as string
        
        #DC Power Distribution over the year
        figDC = px.scatter(df3x, x="TIME", y="EArray", title="DC Power: Daily Distribution", color = "DATE_STR",width=620,height=460)
        figDC.update_traces(marker=dict(size=5, opacity=0.7), selector=dict(mode='markers'))
        colDC.plotly_chart(figDC)
        
        #DC Power Distribution over the year
        figAC = px.scatter(df3x, x="TIME", y="E_Grid", title="AC Power: Daily Distribution", color = "DATE_STR",width=620,height=460)
        figAC.update_traces(marker=dict(size=5, opacity=0.7), selector=dict(mode='markers'))
        colAC.plotly_chart(figAC)
        
        
        
        
        
        

        
    else:
        df=pd.read_csv('data/main_data.csv')
        
        
        df.E_Grid[df.E_Grid.lt(0)] = 0
        df['date'] = pd.to_datetime(df['date'])
        df1 = df.set_index(['date'])
        
        #Metrics-Backend
        df1_sum=df1.sum(axis=0, skipna=True)
        dfd=df[df["E_Grid"] != 0.0].resample('D', on='date').mean()
        Tmod=dfd.TArray.mean()
        dfTamb=df.resample('Y', on='date').mean()
        
        
        #Metrics-Frontend
        col1,col2,col3,col4,col5=st.columns(5)
        col1.metric(label="Total GHI (kWh/m\u00b2/year)", value="{:.2f}".format(df1_sum.GlobHor/1000))
        col2.metric(label="Total GII (kWh/m\u00b2/year)", value="{:.2f}".format(df1_sum.GlobInc/1000))
        col3.metric(label="Annual PR (%)", value="{:.0%}".format(df1_sum.E_Grid*1000/df1_sum.GlobInc/12000))
        col4.metric(label="Yearly Energy Yield (MWh/year)", value="{:.2f}".format(df1_sum.E_Grid/1000))
        col5.metric(label="Yearly Avg PV Temperature (\u00b0C)", value="{:.2f}".format(Tmod))
        
        st.markdown("----------------------------------------")
        
        cols1,cols2,cols4,cols5=st.columns(4)
        cols1.metric(label="Peak GHI(W/m\u00b2)",value="{:.2f}".format(df1.GlobHor.max()))
        cols2.metric(label="Peak GII(W/m\u00b2)",value="{:.2f}".format(df1.GlobInc.max()))
        #cols3.markdown(" ")
        cols4.metric(label="Ambient Temperature(\u00b0C)",value="Max: "+str(float("{:.1f}".format(df1.T_Amb.max())))+"\u00b0C",delta = "Min: "+str(float(df1.T_Amb.min()))+"\u00b0C", delta_color = 'inverse')
        cols5.metric(label="Module Temperature(\u00b0C)",value = "Max: "+str(float("{:.2f}".format(df1.TArray.max())))+"\u00b0C", delta = "Min: "+str(float("{:.2f}".format(df1.TArray.min())))+"\u00b0C", delta_color = 'inverse')
        
        #st.info('Info message')

        

        
        col1,col2=st.columns(2)
        #Irradiance Graph
        fig1 = px.line(df1, y=["GlobInc", "GlobHor"],title='Hourly Solar Irradiance (W/m\u00b2) GII & GHI',width=620,height=460)
        fig1.update_layout(title_text='<b>Hourly Solar Irradiance (W/m\u00b2) GII & GHI</b>', title_x=0.5,
                   xaxis_title="Time (in HH:MM)",yaxis_title="Irradiance (W/m\u00b2)")
        col1.plotly_chart(fig1)
        
        #Temperature Graph
        fig2 = px.line(df1, y=["TArray", "T_Amb"],title='Hourly Temperature Distribution (W/m\u00b2) Ambient & Module Temperature',width=620,height=460)
        fig2.update_layout(title_text='<b>Hourly Temperature Distribution (W/m\u00b2) Ambient & Module Temperature</b>', title_x=0.5,
                   xaxis_title="Time",yaxis_title="Temperature (\u00b0C)")
        col2.plotly_chart(fig2)
        
        col1,col2=st.columns(2)
        col1.info('Info message')
        col2.info('Info message')
        
        st.markdown("----------------------------------------")
        
        cols1,cols2,cols4,cols5=st.columns(4)
        cols1.metric(label="Max DC Power(kW)",value="{:.2f}".format(df1.EArray.max()))
        cols2.metric(label="Max AC Power(kW)",value="{:.2f}".format(df1.E_Grid.max()))
        #cols3.markdown(" ")
        cols4.metric(label="Yearly Avg GII(kWh/m\u00b2/day)",value="{:.2f}".format(df1_sum.GlobInc.mean()/1000))
        cols5.metric(label="Yearly Avg Amb Temperature(\u00b0C)",value ="{:.2f}".format(dfTamb.T_Amb.max())+"\u00b0C")
        
        
        
        colx,coly=st.columns(2)
        #E_Grid & EArray Graph
        figx = px.line(df1, y=["EArray", "E_Grid"],title='Hourly DC & AC Power(kW) Generation Over the Year',width=620,height=460)
        figx.update_layout(title_text='<b>Hourly DC & AC Power(kW) Generation Over the Year</b>', title_x=0.5,
                   xaxis_title="Time",yaxis_title="Power (kW)")
        colx.plotly_chart(figx)
        
        #E_Grid Vs GII Graph
        figy = px.scatter(df1,x="GlobInc", y="E_Grid",title='Hourly AC Power(kW) Vs GII (W/m\u00b2) Plot',width=620,height=460,color='TArray')
        figy.update_layout(title_text='<b>Hourly AC Power(kW) Vs GII (W/m\u00b2) Plot</b>', title_x=0.5,
                   xaxis_title="GII (W/m\u00b2)",yaxis_title="E_Grid (kW)")
        coly.plotly_chart(figy)
 
    
        df3x=df1
        df3x['date'] = df3x.index
        # adding separate time and date columns
        df3x["DATE"] = pd.to_datetime(df3x['date']).dt.date # add new column with date
        df3x["TIME"] = pd.to_datetime(df3x['date']).dt.time # add new column with time
        # add hours and minutes for ml models
        df3x['HOURS'] = pd.to_datetime(df3x['TIME'],format='%H:%M:%S').dt.hour
        df3x['MINUTES'] = pd.to_datetime(df3x['TIME'],format='%H:%M:%S').dt.minute
        df3x['MINUTES_PASS'] = df3x['MINUTES'] + df3x['HOURS']*60

        # add date as string column
        colDC, colAC=st.columns(2)
        df3x["DATE_STR"] = df3x["DATE"].astype(str) # add column with date as string
        
        #DC Power Distribution over the year
        figDC = px.scatter(df3x, x="TIME", y="EArray", title="DC Power: Daily Distribution", color = "DATE_STR",width=620,height=460)
        figDC.update_traces(marker=dict(size=5, opacity=0.7), selector=dict(mode='markers'))
        colDC.plotly_chart(figDC)
        
        #DC Power Distribution over the year
        figAC = px.scatter(df3x, x="TIME", y="E_Grid", title="AC Power: Daily Distribution", color = "DATE_STR",width=620,height=460)
        figAC.update_traces(marker=dict(size=5, opacity=0.7), selector=dict(mode='markers'))
        colAC.plotly_chart(figAC)
        
        
        
        
        
        
        
        
        