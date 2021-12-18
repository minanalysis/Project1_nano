
import pandas as pd
from tqdm import trange
import time
import requests

def metalist(page_no): 
    url='https://api.metaverse2.com/api/v1.0/order/market_list'
    params=f'lastPage=5283&page={page_no}&sort=totalPrice&order=DESC'
    response=requests.get(url,params=params)
    metalist=response.json()
    return pd.DataFrame(metalist)

metabus2=[]

for page_no in trange(1,현 시점기준 마지막페이지수+1):
    temp=metalist(page_no)
    metabus2.append(temp)
    time.sleep(0.01)
    
metabus2_(일시)=pd.concat(metabus2)
metabus2_(일시)
