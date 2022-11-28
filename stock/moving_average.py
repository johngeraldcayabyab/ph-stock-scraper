# The stock price is above both the 150-day and the 200-day moving average.
# The 150-day moving average should be above the 200-day moving average.
# The 200-day moving average line is on an uptrend for at least 1-month. Better if it is for 4 to 5 months.
# The 50-day moving average should be above both the 150 and the 200-day moving averages.
# The existing stock price is at least 25% above its 52-week low.&nbsp;
# The current stock price is within at least 25% of its 52-week high (the closer to a new high the better).
# The relative strength ranking is not less than 70, but preferably in the 90s. The RS Line should also be in an uptrend for at least 6 weeks, preferably 13 weeks.
# The current price is trading above the 50-day moving average as the stock is coming out of a base.&nbsp;

import pandas as pd
import matplotlib.pyplot as plt

# created a time series first

df = pd.read_csv('../../machine-learning-study/csv/ACEN-Historical-Data.csv')
df['Date'] = pd.to_datetime(df['Date'])  # x axis
df = df.sort_values(by='Date')

x = df['Date']
y = df['Open']

print(x.shape[0])
print(y.shape[0])

arr = df['Open']
window_size = 50

# Convert array of integers to pandas series
numbers_series = pd.Series(arr)

# Get the window of series
# of observations of specified window size
windows = numbers_series.rolling(window_size)

# Create a series of moving
# averages of each window
moving_averages = windows.mean()

# Convert pandas series back to list
moving_averages_list = moving_averages.tolist()

# Remove null entries from the list
final_list = moving_averages_list[window_size - 1:]

print(len(final_list))


print(1703 - 1655)

plt.plot(x, y)
plt.show()