import pandas as pd
import matplotlib.pyplot as plt
import numpy
from scipy import stats

<<<<<<< HEAD
df = pd.read_csv('../../machine-learning-study/csv/AC-30dayHistory-Nov02.csv')

df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d %H:%M:%S').dt.strftime('%m-%d')

X = df['Date']
y = df['Close']

plt.plot(df['Close'])

plt.show()
=======
# df = pd.read_csv('../../machine-learning-study/csv/AC-30dayHistory-Nov02.csv')
#
# df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d %H:%M:%S').dt.strftime('%m-%d')
#
# X = df['Date']
# y = df['Close']
#
# plt.plot(df['Close'])
#
# plt.show()
>>>>>>> bf2c97fa3304f6984a81d5a6a45ac6ab345bf988
