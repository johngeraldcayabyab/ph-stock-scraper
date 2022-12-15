import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import numpy
from scipy import stats


def is_close_above_ma(row):
    close = float(row['close'])
    sma_200 = float(row['sma_200'])
    sma_150 = float(row['sma_150'])
    sma_50 = float(row['sma_50'])
    if close > sma_200 and close > sma_150 and close > sma_50:
        return True
    return False


def calculate_close_above_200_150_50_MA(company_id, with_chart=False):
    db_connection_str = 'mysql+pymysql://root@localhost/ph_stock_scraper'
    db_connection = create_engine(db_connection_str)
    sql = 'SELECT * FROM chart_data WHERE company_id = %s ORDER BY chart_date ASC'
    query = pd.read_sql_query(sql=sql, con=db_connection, params=company_id)

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
    count = 0
    lines = []
    start_end = []

    for index, row in df.iterrows():
        if is_close_above_ma(row):
            row['average_above'] = True
            count = 1
            start_end.append({
                'close': row['close'],
                'chart_date': row['chart_date']
            })
        if count and row['average_above'] == False:
            count = 0
            lines.append(start_end)
            start_end = []

    total_days = []
    # print(row)
    for line in lines:
        total_days.append(len(line))
        if with_chart:
            x_values = [line[0]['chart_date'], line[-1]['chart_date']]
            y_values = [line[0]['close'], line[-1]['close']]
            plt.plot(x_values, y_values, linestyle="--")

    print("average days a stock is above the (200,150,50) MA is = ", numpy.average(total_days))
    print(stats.mode(total_days))
    # print(total_days)
    # print(len(total_days))

    if with_chart:
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

    return numpy.average(total_days)


calculate_close_above_200_150_50_MA("2")
