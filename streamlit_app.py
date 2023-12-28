import streamlit as st
from collections import namedtuple
import math
import pandas as pd
import numpy as np
import plost                # this package is used to create plots/charts within streamlit
from PIL import Image       # this package is used to put images within streamlit
import altair as alt
import matplotlib
import matplotlib.pyplot as plt 
from datetime import date, datetime, timedelta
from api_connection import get_data_from_api       # keep this commented if not using it otherwise brakes the app
import random 

# Page setting
st.set_page_config(layout="wide")

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# DATA EXTRACT
Price_v, Times_v = get_data_from_api() # 10 1st values ; [67 65 63 63 60 67 68 111 150 100 ... 94] CONSIDERED AS [€/MWh / each hour] => f(t)

for j in range(len(Price_v)):
    Price_v[j] /= 1000 # [€/kWh]
    Price_v[j] = round(Price_v[j],3)


# PYTHON CODE TO DEVELOP FOR PROJECT WITH LINK WITH ARDUINO ############################################################################
# MACRO 
BUDGET = 200 # [€/ month]          
BUDGET_UNIT = round(BUDGET/(31*24),2) # [€/h]
BUD_UNIT_V = [BUDGET_UNIT] * 24


                                                                # ON THE GRAPH : 

# 1st curve - Electricity price each hour f(t) => [€/kWh/h]
#Price_v  # [€/kWh/h]

# Here needed to extract the POWER at each hour [kWh] from Arduino => Need to change every hour (real); so every 30sec for the demosntration 
# The loop will read the signal from arduino every 30sec , increment the vector Price_v and the vector Energy_inst and the Times2 also .
Energy_inst = [round(random.uniform(1.5, 4.5),2) for _ in range(24)]  # [kWh] 

# 2nd curve - Instantaneous consumption  : 
#i=0 #random value for now
if len(Price_v) == len(Energy_inst):
    Consume_now = []  # Initialisation de la liste Consume_now

    for i in range(len(Price_v)):
        result = round(Price_v[i] * Energy_inst[i], 2)  
        Consume_now.append(result)
# 3rd curve - budget limit 
#BUDGET_UNIT                                 #  [€/h] 

                                                                # BONUS UPDATED MONEY SAVINGS :

# current_hour is the hour we are , at each iteration ABBAS, u have to run this loop to sum the money saved :
current_hour = 22
money_saved = 0
for k in range(current_hour): 
    delta = BUDGET_UNIT - Consume_now[k]
    money_saved += delta

money_saved = round(money_saved,2)

# END DEVELOP ###############################################################################################################################

### WEB APP DESIGN
# Row A
a1, a2, a3 = st.columns(3)
a1.image(Image.open('streamlit-logo-secondary-colormark-darktext.png'))
a2.metric("Monthly Budget", str(BUDGET) + " €/month ", "Fixed by the consumer")
a3.metric("Hourly Budget", str(BUDGET_UNIT) + " €/hour ", "Fixed by the consumer")

# Row B
b1, b2, b3, b4 = st.columns((2, 2, 2, 2))
b1.metric("PVPC Price instantaneous", str(Price_v[0]) + " €/kwh/hour", "From API")
b2.metric("House instantaneous  energy consumption", str(Energy_inst[0]) + " kWh", "From Arduino by Current Sensor")
b3.metric(" Current Price spending", str(Consume_now[0]) + "€/hour", " ")
b4.metric("DATETIME", str(Times_v[2]), " ")

# Row C
c1, c2 = st.columns((4,2))

# HERE YOU NEED TO LINK THE DYNAMIC ACTUALISATION OF THE GRAPH WITH ARDUINO
with c1: 
    fig, ax = plt.subplots(figsize=(12, 6))  # Définir la taille du graphique
    ax.plot(Times_v, Price_v, label='PVPC Price [€/kwh]', color='blue')  # Première fonction en bleu
    ax.plot(Times_v, BUD_UNIT_V, label='Budget [€]', color='red')   # Deuxième fonction en rouge
    ax.plot(Times_v, Consume_now, label='Current Price spending [€]', color='green') # Troisième fonction en vert

    # ADD
    ax.tick_params(axis='x', rotation=45)
    ax.legend()  # Afficher la légende avec les noms des fonctions
    #ax.set_title('Tracé de trois fonctions différentes')
    ax.set_xlabel('Datetime')
    ax.set_ylabel('Data')
    ax.grid(True)  # Ajouter une grille

    # Afficher le graphique dans Streamlit
    st.pyplot(fig)

with c2: 
    c2.metric(" MONEY SAVINGS / LOSTS ", str(money_saved) + " € ", " Updated each hour (in progress..) " )
