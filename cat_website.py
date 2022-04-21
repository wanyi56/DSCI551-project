#!/usr/bin/env python
# coding: utf-8




import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import csv
import json
import requests
import sys
import price
import filter

#title

st.title('Cat Can food nutrition')

url = 'https://dsci551-project-d7a1a-default-rtdb.firebaseio.com/.json'
response = requests.get(url)
js = response.json()
data = pd.DataFrame(js)
data['COMPANY'] = data['COMPANY'].apply(lambda x: ' '.join(x.split()))

#set selectbar in the sidebar

brand = pd.unique(data['COMPANY'])
brand = np.insert(brand,0,'SELECT')

company = st.sidebar.selectbox(
    "Select Company",
    (brand)
)
flavor = ['SELECT','beef','chicken','tuna','turkey','crab','shrimp','pork','liver','duck','lamb','salmon','fish']

flavor = st.sidebar.selectbox(
    "Select flavor",
    flavor
)



notes = st.sidebar.selectbox(
    "doctor notes",(['SELECT','Yes','No'])
)


#set range slider in the sidebar

protein = st.sidebar.slider(
     'Select a range of protein%',
     0.0, 100.0, (0.0,100.0))
st.sidebar.write('Range:', protein)

fat = st.sidebar.slider(
     'Select a range of fat%',
     0.0, 100.0, (0.0,100.0))
st.sidebar.write('Range:', fat)

carb = st.sidebar.slider(
     'Select a range of carb%',
     0.0, 100.0, (0.0,100.0))
st.sidebar.write('Range:', carb)


# show dataframe in the website

if company == 'SELECT':
      company = ''

if flavor == 'SELECT':
      flavor = ''
if notes == 'SELECT':
      pre = ""
if notes == 'Yes':
      pre = "Cat is not null and "
if notes == 'No':
      pre = "Cat is null and "


st.dataframe(filter.filter_df(company,flavor,pre,protein[0],protein[1],fat[0],fat[1],carb[0],carb[1]),width=1000,height=1000)



#insert price searching

p = st.text_input("search the price")


if st.button('Search'):
     lst = price.search_price(p)
     st.dataframe(lst[0],width=1000,height=1000)
     st.write('The search result may differ from actual price. Please refer to the websites for the actual price.')
     st.write('Chewy: '+lst[1])
     st.write('Petsmart: '+lst[2])
     st.write('Petco: '+lst[3])

#insert an image
st.image('https://i.imgur.com/vuYRIOH.jpg', caption='a furry friend')
