#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import sys
import json
import sqlalchemy
import pandas as pd
import os.path


# In[2]:


#先把firebase变成dataframe


# In[3]:


url = 'https://dsci551-project-d7a1a-default-rtdb.firebaseio.com/.json'
response = requests.get(url)
js = response.json()


# In[4]:


#原表格名字太多空格不适合当sql的指令，先改一改，最后换回来


# In[5]:


df = pd.DataFrame(js)
column1  = df.columns
df = df.rename(lambda x: x[0:3],axis='columns')
column2 = df.columns

df['COM'] = df['COM'].apply(lambda x: ' '.join(x.split()))



#把dataframe变成sql


# In[7]:



# In[8]:

if os.path.exists("data.db") == False:
    engine = sqlalchemy.create_engine("sqlite:///data.db")
    food_info = df.to_sql("info",con=engine,index=False)


# In[17]:


#这条括号输入指令可以展示sql 的table变成什么样了在这里验证sql 的指令


# In[54]:


engine.execute("select * from info where FLA like '%Chicken%'").fetchall()


# In[ ]:


#把sql的table变回dataframe，从这里开始开始写def，把sql 指令换成你上面验证OK的,并把变量改成def的input，要return dataframe


# In[9]:


def filter_df(company,flavor,pre,pro_0,pro_1,fat_0,fat_1,car_0,car_1):
    query = "select * from info where (COM like '%{0}%') and (FLA like '%{1}%') and {2}(PRO between {3} and {4}) and (FAT between {5} and {6}) and (CAR between {7} and {8})".format(company,flavor,pre,pro_0,pro_1,fat_0,fat_1,car_0,car_1)
    output = pd.read_sql(query,con=engine,index_col=None)
    output = output.rename(columns={'COM':'COMPANY','FLA':'FLAVOR or STYLE','PRO':'PROTEIN (percent)','FAT':'FAT (percent)','CAR':'CARB (percent)', 'mg ':'mg PHOS per 100 kcals','Cat':'Cat food nutritional composition'})
    return output


# In[67]:



