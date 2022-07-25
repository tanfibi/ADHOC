import numpy as np
import pandas as pd
import json
import re


df = pd.read_json('transactions.json')

filter = df[['transaction_items', 'transaction_value']].copy()

sanitize = df[['transaction_date', 'transaction_items']].copy()
sanitize['transaction_date'] = pd.to_datetime(sanitize.transaction_date).dt.strftime('%m')

df_product_price = filter[(filter['transaction_items'].str.contains('(x1)')) & (~filter['transaction_items'].str.contains(';')) ].drop_duplicates().reset_index(drop=True)
    

month = []
productsPrice = {}
productsTotal = {}


for i, row in df_product_price.iterrows():        
    z = re.search('^(.*?),\(', df_product_price.at[i,'transaction_items']).group(1)     
    if (str(z) not in productsPrice) :
        productsPrice[str(z)] = df_product_price.at[i, 'transaction_value']
    if (str(z) not in productsTotal) :
        productsTotal[str(z)] = [0] * 12 
        
sanitize['transaction_items'] = sanitize['transaction_items'].str.split(';')
sanitize = sanitize.explode('transaction_items').reset_index(drop=True)

for i, row in sanitize.iterrows():
        
    y = re.search('\(x([^)]+)', sanitize.at[i,'transaction_items']).group(1)        
    z = re.search('^(.*?),\(', sanitize.at[i,'transaction_items']).group(1) 
    monthSold = sanitize.at[i,'transaction_date']
    
    productsTotal.get(str(z))[int(monthSold)-1] += (int(y) * int(productsPrice.get(str(z))))
    
parsed_df_sum = pd.DataFrame.from_dict(productsTotal, orient='index')
parsed_df_sum