import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('../../machine-learning-study/csv/ACEN-Historical-Data.csv')
df['Date'] = pd.to_datetime(df['Date'])
df['Close'] = 0

for i in range(0, len(df)):
    previousRow = i - 1
    if previousRow in df.index:
        df.loc[i, 'Close'] = df.loc[previousRow, 'Open']
    else:
        df.loc[i, 'Close'] = 0

df = df.sort_values(by='Date')

df = df.set_index(df['Date'])

close = df['Close']
close_50_ma = close.rolling(window=50).mean()
close_150_ma = close.rolling(window=150).mean()
close_200_ma = close.rolling(window=200).mean()

plt.plot(close, 'k-', label='Original')
plt.plot(close_50_ma, 'g-', label='50 Day MA')
plt.plot(close_150_ma, 'r-', label='150 Day MA')
plt.plot(close_200_ma, 'b-', label='200 Day MA')

plt.ylabel('Price')
plt.xlabel('Date')

plt.grid(linestyle=':')

plt.fill_between(close_50_ma.index, 0, close_50_ma, color='g', alpha=0.1)
plt.fill_between(close_150_ma.index, 0, close_150_ma, color='r', alpha=0.1)
plt.fill_between(close_200_ma.index, 0, close_150_ma, color='b', alpha=0.1)

plt.legend(loc='upper left')

plt.show()
