import numpy as np
import pandas as pd
import json
import re
from datetime import datetime

df = pd.read_json('transactions.json')

sanitize = df[['name', 'transaction_date']].copy()
sanitize['transaction_date'] = pd.to_datetime(sanitize.transaction_date).dt.strftime('%m')
sanitize = sanitize.drop_duplicates()

multi_group = sanitize.groupby(['name'])['transaction_date'].apply(','.join).reset_index()

maxMonth = int(sanitize['transaction_date'].max())

month = []
status = {}

def repeater( monthList ):
    x = 0    
    for month in monthList:
        if ( x != 0 ): 
            if ( int(monthList[x-1]) == int(month)-1 ): 
                status.get('repeaters')[int(month)-1] += 1 
        
        x += 1

 #-------------------------------------------------------------------------
    
def inactive( monthList ):
    monthCount = len(monthList)
    y = 0;
    isEarliestMonth = True
    
    for x in range(maxMonth):
        if (x == (int(monthList[y])-1)) :            
            if (y+1 < monthCount):
                y += 1
            if (isEarliestMonth == True): 
                isEarliestMonth = False
        else:
            if (isEarliestMonth == False):
                status.get('inactive')[x] += 1

#-------------------------------------------------------------------------

def engaged( monthList ):
    x = 1 
        
    startedOnJanuary = False
    
    for month in monthList: 
        if ( int(month) == 1 ) :
            startedOnJanuary = True
            
        if ( startedOnJanuary and x == int(month) ): 
            x += 1 
        
    
    if ( startedOnJanuary and x == len(monthList) ): 
        for month in monthList:
            status.get('engaged')[int(month)-1] += 1

#-------------------------------------------------------------------------

status['repeaters'] = [0] * 12
status['inactive'] = [0] * 12
status['engaged'] = [0] * 12

for i, row in multi_group.iterrows():    
    monthList = row['transaction_date'].split(",") 
    repeater( monthList )
    engaged( monthList )
    inactive( monthList )

parsed_df_customers = pd.DataFrame.from_dict(status, orient='index') 

parsed_df_customers