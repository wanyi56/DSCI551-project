#!/usr/bin/env python
# coding: utf-8

# In[1]:

import requests
import sys
import json
import sqlalchemy
import pandas as pd
import os.path

#transfer firebase to dataframe

url = 'https://dsci551-project-d7a1a-default-rtdb.firebaseio.com/.json'
response = requests.get(url)
js = response.json()


# rename column names to make the sql query to be easy


df = pd.DataFrame(js)
column_names = ["COMPANY", "FLAVOR or STYLE", "PROTEIN(percent)","FAT(percent)", "CARB(percent)","mg PHOS per 100 kcals","Cat food nutritional composition"]
df = df.reindex(columns=column_names)
column1  = df.columns
df = df.rename(lambda x: x[0:3],axis='columns')
column2 = df.columns

df['COM'] = df['COM'].apply(lambda x: ' '.join(x.split()))



#tranform dataframe to sql


if os.path.exists("data.db") == False:
    engine = sqlalchemy.create_engine("sqlite:///data.db")
    food_info = df.to_sql("info",con=engine,index=False)

engine = sqlalchemy.create_engine("sqlite:///data.db")

# define filter function

def filter_df(company,flavor,pre,pro_0,pro_1,fat_0,fat_1,car_0,car_1):
    query = "select * from info where (COM like '%{0}%') and (FLA like '%{1}%') and {2}(PRO between {3} and {4}) and (FAT between {5} and {6}) and (CAR between {7} and {8})".format(company,flavor,pre,pro_0,pro_1,fat_0,fat_1,car_0,car_1)
    output = pd.read_sql(query,con=engine,index_col=None)
    output = output.rename(columns={'COM':'COMPANY','FLA':'FLAVOR or STYLE','PRO':'PROTEIN (percent)','FAT':'FAT (percent)','CAR':'CARB (percent)', 'mg ':'mg PHOS per 100 kcals','Cat':'Cat food nutritional composition'})
    return output


# output dataframe
