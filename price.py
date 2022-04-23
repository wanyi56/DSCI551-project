#!/usr/bin/env python
# coding: utf-8

# In[3]:

from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from bs4 import BeautifulSoup
import pandas as pd
import sys
import os
import streamlit as st
# In[8]:
@st.experimental_singleton
def installff():
    os.system('sbase install geckodriver')
    os.system('ln -sf /home/appuser/venv/lib/python3.7/site-packages/seleniumbase/drivers/geckodriver /home/appuser/venv/bin/geckodriver')

_ = installff()
opt = webdriver.FirefoxOptions()
opt.add_argument('--headless')
opt.add_argument('--ignore-certificate-errors')
opt.add_argument('--allow-running-insecure-content')
user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
opt.add_argument(f'user-agent={user_agent}')


# In[38]:

def chewy(k,out_queue):


    # chewy
    driver_chewy = webdriver.Firefox(options=opt)
    # chewy

    url_chewy = "https://www.chewy.com/s?query=cat%20wet%20food%20"+k+"&nav-submit-button="
    driver_chewy.get(url_chewy)
    website_chewy = []
    prices_chewy = []
    names_chewy = []

    content_chewy = driver_chewy.page_source
    soup_chewy = BeautifulSoup(content_chewy,"html.parser")
    n = soup_chewy.findAll('div',attrs={'class':'ProductListing_kibProductCard__3KgKt js-tracked-product kib-product-card'})
    if len(n) != 0:
        for a in n[:min(5,len(n))-1]:
            price=a['data-price']
            name=a['data-name']

            website_chewy.append('chewy')
            prices_chewy.append(price)
            names_chewy.append(name.strip())

    else:
        website_chewy = 'chewy'
        prices_chewy = 'no result'
        names_chewy = 'no result'


    d = {'Name':names_chewy,'Price':prices_chewy,'Sold by':website_chewy}
    df = pd.DataFrame(d)

    out_queue.put([df,url_chewy])






# In[39]:



def petsmart(k,out_queue):    #petsmart


    driver_petsmart = webdriver.Firefox(options=opt)
    url_petsmart = "https://www.petsmart.com/search/?q=cat%20wet%20food%20"+k+"&ps=undefined"
    driver_petsmart.get(url_petsmart)

    website_petsmart = []
    prices_petsmart = []
    names_petsmart = []

    content_petsmart = driver_petsmart.page_source
    soup_petsmart = BeautifulSoup(content_petsmart,"html.parser")
    n = soup_petsmart.findAll('li',attrs={'class':'grid-tile gtm-grid-tile col-md-4 col-sm-12'})
    if len(n) != 0:
        for a in n[:min(5,len(n))-1]:
            price=a.find('span', attrs={'class':'price-regular'})
            if not price:
                price=a.find('span', attrs={'class':'price-sales'})
            name=a.find('div', attrs={'class':'product-name'})

            website_petsmart.append('petsmart')
            prices_petsmart.append(price["data-gtm-price"])
            names_petsmart.append(name.text.strip())

    else:
        website_petsmart = 'petsmart'
        prices_petsmart = 'no result'
        names_petsmart = 'no result'


    d = {'Name':names_petsmart,'Price':prices_petsmart,'Sold by':website_petsmart}
    df = pd.DataFrame(d)

    out_queue.put([df,url_petsmart])


# In[40]:



def petco(k,out_queue):    #petco


    driver_petco = webdriver.Firefox(options=opt)



    url_petco = "https://www.petco.com/shop/SearchDisplay?categoryId=&storeId=10151&catalogId=10051&langId=-1&sType=SimpleSearch&resultCatEntryType=2&showResultsPage=true&searchSource=Q&pageView=&beginIndex=0&pageSize=48&fromPageValue=search&searchKeyword=&searchTerm=cat%20wet%20food%20"+k
    driver_petco.get(url_petco)

    website_petco = []
    prices_petco = []
    names_petco = []

    content_petco = driver_petco.page_source
    soup_petco = BeautifulSoup(content_petco,"html.parser")
    n = soup_petco.findAll('div',attrs={'class':'product-info'})
    if len(n) != 0:
        for a in n[:min(5,len(n))-1]:
            price=a.find('span', attrs={'class':'product-price-promo'})
            name=a.find('div', attrs={'class':'product-name'})
            website_petco.append('Petco')
            prices_petco.append(price.text.strip())
            names_petco.append(name.text.strip())

        names_petco = [a.replace("\n", " ") for a in names_petco]
    if len(n) == 0:
        website_petco = ['petco']
        prices_petco = ['no result']
        names_petco = ['no result']






    d = {'Name':names_petco,'Price':prices_petco,'Sold by':website_petco}
    df = pd.DataFrame(d)

    out_queue.put([df,url_petco])


# In[ ]:
from threading import Thread
import queue

@st.cache(ttl=60)
def search_price(k):
    k = k.replace(' ','%20')
    my_queue1 = queue.Queue()
    my_queue2 = queue.Queue()
    my_queue3 = queue.Queue()

    ret_1 = Thread(target = petsmart,args=(k,my_queue1))
    ret_2 = Thread(target = chewy,args=(k,my_queue2))
    ret_3 = Thread(target = petco,args=(k,my_queue3))
    ret_1.start()
    ret_2.start()
    ret_3.start()

    ret1 = my_queue1.get()
    ret2 = my_queue2.get()
    ret3 = my_queue3.get()

    ret_1.join()
    ret_2.join()
    ret_3.join()

    result = [pd.concat([ret1[0],ret2[0],ret3[0]]),ret1[1],ret2[1],ret3[1]]
    return result

# In[ ]:





# In[ ]:





# In[ ]:





# In[41]:





# In[ ]:





# In[ ]:
