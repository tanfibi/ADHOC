import numpy as np
import pandas as pd
import json
import re
from datetime import datetime

df = pd.read_json('transactions.json')
month = []
products = {}

for i, row in df.iterrows():

    for x in df.at[i,'transaction_items'].split(";"): 
        y = re.search('\(x([^)]+)', x).group(1) 
        z = re.search('^(.*?),\(', x).group(1) 
        
        if (str(z) not in products) :
            products[str(z)] = [0] * 12
        
        
        date = str(df.at[i,'transaction_date']) #get date sold
        dt = datetime.strptime(date, '%Y/%m/%d') #parse date sold and get the month
        #print( int(dt.month) )
    
        products.get(str(z))[int(dt.month)-1] += int(y) 
        
    
parsed_df_productsold = pd.DataFrame.from_dict(products, orient='index')
parsed_df_productsold