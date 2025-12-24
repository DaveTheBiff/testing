'''
Objective: Aggregation and Reporting. 
Using the cleaned dataset from Task 2 (assuming you have expanded it to more rows),

Requirements:
1.  Group the data by category.
2.  Calculate the Total Revenue (Sum of Price) and Average Price for each category.
3.  Export this summary to a CSV file named executive_summary.csv.
4.  Crucial Step: Ensure the index is NOT saved as a column in the output file. 
'''

# ========== Solution ==========

import pandas as pd
import numpy as np

# expanded data set, but the first 4 is the cleaned data from Task 2
data = {
    'id': [1, 2, 3, 4, 5, 6, 7, 8],
    'price': [1000.0, 2500.0, np.nan, 500.0, 1200.0, 3000.0, 800.0, 2200.0],
    'date': pd.to_datetime(['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04', 
                            '2023-01-05', '2023-01-06', '2023-01-07', '2023-01-08']),
    'category': ['Hardware', 'Software', 'Hardware', 'Unknown', 'Hardware', 'Software', 'Software', 'Hardware']
}
df = pd.DataFrame(data)

# 1. Group by category and calculate Total Revenue and Average Price
summary_df = df.groupby('category')['price'].agg(['sum', 'mean']).reset_index()

# 2. Rename columns for clarity
summary_df.columns = ['Category', 'Total Revenue', 'Average Price']

# 3. Export to CSV file
summary_df.to_csv('executive_summary.csv', index=False)

print(summary_df)