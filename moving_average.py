import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt

db_connection_str = 'mysql+pymysql://root@localhost/ph_stock_scraper'
db_connection = create_engine(db_connection_str)
query = pd.read_sql('SELECT * FROM chart_data WHERE company_id = 1 order by chart_date asc', con=db_connection)

df = query['close'].to_frame()

df['sma_200'] = df['close'].rolling(200).mean()
df['sma_150'] = df['close'].rolling(150).mean()
df['sma_50'] = df['close'].rolling(50).mean()
df['chart_date'] = pd.to_datetime(query['chart_date'])
df['average_above'] = False

df = df.sort_values(by='chart_date')

df = df.set_index(df['chart_date'])

# removing all the NULL values using
# dropna() method
df.dropna(inplace=True)

# print(type(df))
#
# this should be the code that would draw lines on when all the things is correct below
lines = []

for index, row in df.iterrows():
    close = float(row['close'])
    sma_200 = float(row['sma_200'])
    sma_150 = float(row['sma_150'])
    sma_50 = float(row['sma_50'])
    # row['average_above'] = False
    # line = {'point_1': 0, 'point_2': 0}
    # line = []
    if close > sma_200 and close > sma_150 and close > sma_50:
        lines.append(row['close'])
        # print(1)
        # line['point_1'] = row['close']
        # if row['average_above']:
        #
        # row['average_above'] = True
        # print(close, row['chart_date'])


    # print(row)
print(lines)


plt.plot(df['close'], 'k-', label='Original')
plt.plot(df['sma_50'], 'g-', label='50 Day MA')
plt.plot(df['sma_150'], 'r-', label='150 Day MA')
plt.plot(df['sma_200'], 'b-', label='200 Day MA')

plt.ylabel('Price')
plt.xlabel('Date')

plt.ylabel('Price')
plt.xlabel('Date')

plt.grid(linestyle=':')

plt.fill_between(df['sma_50'].index, 0, df['sma_50'], color='g', alpha=0.1)
plt.fill_between(df['sma_150'].index, 0, df['sma_150'], color='r', alpha=0.1)
plt.fill_between(df['sma_200'].index, 0, df['sma_200'], color='b', alpha=0.1)

plt.legend(loc='upper left')

plt.show()
