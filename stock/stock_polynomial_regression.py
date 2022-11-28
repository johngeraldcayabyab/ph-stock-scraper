import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import datetime, time

df = pd.read_csv('../../machine-learning-study/csv/AC-30dayHistory-Nov02.csv')

df['Date'] = pd.to_datetime(df['Date'])  # x axis
df = df.sort_values(by='Date')
df['Date'] = (df['Date'] - pd.Timestamp("1970-01-01")) // pd.Timedelta('1s')



curve = np.polyfit(df['Date'], df['Close'], 2)
poly = np.poly1d(curve)


df['Close'] = df['Close'].astype(np.int64)


line = np.linspace(df['Date'].iat[0], df['Date'].iat[-1], df['Close'].iat[-1])

print(df['Close'])

plt.scatter(df['Date'], df['Close'])
plt.plot(line, poly(line))
plt.show()




# print(poly)

# date = df['Date']
# newColumn = df['T'].
# close = df['Close']
#
# print(df['Date'])

# model = numpy.poly1d(numpy.polyfit(date, close, 3))

# line = numpy.linspace(date.iat[0], date.iat[-1])

# plt.scatter(date, close)
# plt.plot(line, model(line))
# plt.show()
