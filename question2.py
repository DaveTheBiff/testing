'''
Objective: Handle mixed types and missing data. 
You are given a raw CSV snippet below. It mimics real-world dirty data (currency symbols, inconsistent dates, missing values). 

# raw_data.csv content simulation 
data = { 
'id': [1, 2, 3, 4], 
'price': ['$1 ,000', '$2 ,500', 'Not Available', '$500'], 
'date': ['01/01/2023', '2023 -01 -02', 'Jan 3, 2023', '01/04/2023'], 
'category': ['Hardware', 'Software', 'Hardware', None] 
} 
'''

# ========== Solution ==========

import pandas as pd
import numpy as np

# raw_data.csv content simulation
data = {
    'id': [1, 2, 3, 4],
    'price': ['$1 ,000', '$2 ,500', 'Not Available', '$500'],
    'date': ['01/01/2023', '2023 -01 -02', 'Jan 3, 2023', '01/04/2023'],
    'category': ['Hardware', 'Software', 'Hardware', None]
}

df = pd.DataFrame(data)

# 1. price cleaning
df['price'] = (
    df['price']
    .replace('Not Available', np.nan)
    .str.replace(r'[$, ]', '', regex=True)
    .astype(float)
)

# 2. date cleaning
df['date'] = pd.to_datetime(
    df['date'].str.replace(' ', ''), 
    format='mixed', 
    dayfirst=False
)

# 3. category cleaning
df['category'] = df['category'].fillna('Unknown')

print(df)