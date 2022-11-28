import pandas as pd
import matplotlib.pyplot as plt

# created a time series first
df = pd.read_csv('../../machine-learning-study/csv/ACEN-Historical-Data.csv')
# make date to dt object to become sortable
df['Date'] = pd.to_datetime(df['Date'])  # x axis
# add closing price colum
df['Close'] = 0

for i in range(0, len(df)):
    print(df.loc[i, 'Date'])
    previousRow = i - 1
    if previousRow in df.index:
        df.loc[i, 'Close'] = df.loc[previousRow, 'Open']
    else:
        df.loc[i, 'Close'] = 0


df = df.sort_values(by='Date')
