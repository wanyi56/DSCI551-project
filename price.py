#!/usr/bin/env python
# coding: utf-8

# In[3]:

from selenium import webdriver
import chromedriver_binary
from bs4 import BeautifulSoup
import pandas as pd
import sys
import ray
import os

# In[8]:


options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--allow-running-insecure-content')
user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
options.add_argument(f'user-agent={user_agent}')


# In[38]:


@ray.remote
def chewy(k):
    

    # chewy
    driver_chewy = webdriver.Chrome(executable_path = os.path.abspath("chromedriver.exe"),  chrome_options=options)
    # chewy
    
    url_chewy = "https://www.chewy.com/s?query=cat%20can%20"+k+"&nav-submit-button="
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
            prices_chewy.append('$'+price)
            names_chewy.append(name.strip()) 

    else:
        website_chewy = 'chewy'
        prices_chewy = 'no result'
        names_chewy = 'no result'
    
    
    d = {'Name':names_chewy,'Price':prices_chewy,'Sold by':website_chewy}
    df = pd.DataFrame(d)
    
    return [df,url_chewy]
    
       

    


# In[39]:


@ray.remote
def petsmart(k):    #petsmart
    driver_petsmart = webdriver.Chrome(executable_path = os.path.abspath("chromedriver.exe", chrome_options=options)
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
        
            website_petsmart.append('pet-smart')
            prices_petsmart.append('$'+price["data-gtm-price"])
            names_petsmart.append(name.text.strip()) 

    else:
        website_petsmart = 'petsmart'
        prices_petsmart = 'no result'
        names_petsmart = 'no result'

    
    d = {'Name':names_petsmart,'Price':prices_petsmart,'Sold by':website_petsmart}
    df = pd.DataFrame(d)
    
    return [df,url_petsmart]


# In[40]:


@ray.remote
def petco(k):    #petco
    driver_petco = webdriver.Chrome(executable_path = os.path.abspath("chromedriver.exe", chrome_options=options)



    url_petco = "https://www.petco.com/shop/SearchDisplay?categoryId=&storeId=10151&catalogId=10051&langId=-1&sType=SimpleSearch&resultCatEntryType=2&showResultsPage=true&searchSource=Q&pageView=&beginIndex=0&pageSize=48&fromPageValue=search&searchKeyword=&searchTerm="+k
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
    
    return [df,url_petco] 


# In[ ]:


def search_price(k):
    k = k.replace(' ','%20')
    
    ray.shutdown()
    
    ray.init()
    ret_id1 = chewy.remote(k)
    ret_id2 = petsmart.remote(k)
    ret_id3 = petco.remote(k)
    ret1, ret2, ret3 = ray.get([ret_id1, ret_id2, ret_id3])
    
    result = [pd.concat([ret1[0],ret2[0],ret3[0]]),ret1[1],ret2[1],ret3[1]]
    return result


# In[ ]:





# In[ ]:





# In[ ]:





# In[41]:





# In[ ]:





# In[ ]:




