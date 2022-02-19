# -*- coding: utf-8 -*-
"""
Created on Wed Feb 16 21:52:27 2022

@author: Vladi
"""

import streamlit as st
from streamlit_folium import folium_static
import folium
import geopandas
import random
from folium import plugins
import time
import os

directory = os.getcwd()
FILL_NAME = '#######'

def show_country(country_id):
    m = folium.Map(
        location=[20.70, 30.94], 
        tiles=r'https://{s}.basemaps.cartocdn.com/light_nolabels/{z}/{x}/{y}{r}.png', attr='<a href=https://leaflet-extras.github.io/leaflet-providers/preview//>Endless Sky</a>')
    
    minimap = plugins.MiniMap()
    m.add_child(minimap)
    
    gdf = df.loc[country_id:country_id].copy()
    
    for _,country in gdf.iterrows():
        sim_geo = geopandas.GeoSeries (gdf['geometry']).simplify(tolerance = 0.001)
        geo_j = sim_geo.to_json()
        geo_j = folium.GeoJson(
            data = gdf,
            style_function = lambda x: {'fillColor' : 'orange'})
#        geo_j.add_child(folium.Popup(country['name']))
        geo_j.add_to(m)
        
    m.fit_bounds(m.get_bounds())
    return m

path_to_file = os.path.join(directory,'world-countries.json')

df = geopandas.read_file(path_to_file) 

number_countries = len(df)

if 'score' not in st.session_state:
    st.session_state['score'] = 0
if 'right_answer' not in st.session_state:
    st.session_state['right_answer'] = ''
if 'time_left' not in st.session_state:
    st.session_state['time_left'] = 11
if 'guess' not in st.session_state:
    st.session_state['guess'] = FILL_NAME
if 'lives' not in st.session_state:
    st.session_state['lives'] = 3
if 'best_score' not in st.session_state:
    st.session_state['best_score'] = 0

#st.session_state

next_try = True

countdown = st.empty()
score_holder = st.empty()
lives_holder = st.empty()
country_holder = st.empty()
radio_holder = st.empty()
next_guess=st.empty()

while st.session_state['lives']>0 and next_try:
    
    if st.session_state['right_answer'] == st.session_state['guess'] and\
        st.session_state['guess']!=FILL_NAME and st.session_state['time_left']>0:
            st.session_state['score'] += st.session_state['time_left']*10
            if st.session_state['best_score'] < st.session_state['score']:
                st.session_state['best_score'] = st.session_state['score']
    elif st.session_state['time_left'] == 0 or st.session_state['guess']!=FILL_NAME and\
            st.session_state['right_answer'] != st.session_state['guess']:
             st.session_state['lives']-=1       
             
    score_holder.markdown(f"Current score: {st.session_state['score']}")
    lives_holder.markdown(f"Lives left: {st.session_state['lives']}")
    
    next_try = False    
    
    if st.session_state['lives']>0:
        
        country_id = random.randint(0,number_countries-1)
        
        folium_static(show_country(country_id))
        
        st.session_state['right_answer'] = df.iloc[country_id][1]
        possible_options = [st.session_state['right_answer']]
        
        while len(possible_options)<4:
            random_country = df.iloc[random.randint(0,number_countries-1)][1]
            if random_country not in possible_options:
                possible_options.append(random_country)
        random.shuffle(possible_options)
        
        possible_options.insert(0,FILL_NAME)
        
        radio_holder.radio(
            label = 'Which country is it?', 
            options = possible_options,
            key = 'guess'
            )

        start = time.time()
        while time.time()-start<=11 and st.session_state['guess'] == FILL_NAME:
            st.session_state['time_left'] = round(11 - (time.time()-start))
            countdown.markdown(f"Time left: {st.session_state['time_left']} seconds")              
    else:
        next_guess.write('Thanks for playing')
        st.write(f"Your final score is {st.session_state['score']}")
        st.write(f"Your best score is {st.session_state['best_score']}")
else:
    next_try = next_guess.button('next country?')
    if next_try and st.session_state['lives'] == 0:
        if st.session_state['time_left'] == 0:
            st.session_state['lives'] = 4
        else:
            st.session_state['lives'] = 3
        st.session_state['score'] = 0




    



