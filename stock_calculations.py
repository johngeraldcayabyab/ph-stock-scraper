import math

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
from sqlalchemy import create_engine
from redis import Redis
from rq import Queue

from db import test_connection


def is_close_above_ma(row):
    close = float(row['close'])
    sma_200 = float(row['sma_200'])
    sma_150 = float(row['sma_150'])
    sma_50 = float(row['sma_50'])
    if close > sma_200 and close > sma_150 and close > sma_50:
        return True
    return False


def rma(x, n, y0):
    a = (n - 1) / n
    ak = a ** np.arange(len(x) - 1, -1, -1)
    return np.r_[np.full(n, np.nan), y0, np.cumsum(ak * x) / ak / n + y0 * a ** np.arange(1, len(x) + 1)]


def minervini_scanner(company_id, with_chart=False):
    db_connection_str = 'mysql+pymysql://root@localhost/ph_stock_scraper'
    db_connection = create_engine(db_connection_str)
    sql = 'SELECT * FROM chart_data WHERE company_id = {0} ORDER BY chart_date ASC'.format(company_id)
    query = pd.read_sql_query(sql=sql, con=db_connection)

    df = query['close'].to_frame()

    df['sma_200'] = df['close'].rolling(200).mean()
    df['sma_150'] = df['close'].rolling(150).mean()
    df['sma_50'] = df['close'].rolling(50).mean()
    df['chart_date'] = pd.to_datetime(query['chart_date'])
    df['volume'] = query['volume']
    df['average_above'] = False

    df = df.sort_values(by='chart_date')

    df = df.set_index(df['chart_date'])

    # removing all the NULL values using
    # dropna() method
    df.dropna(inplace=True)

    window_length = 14

    df['change'] = df['close'].diff()
    df['gain'] = df.change.mask(df.change < 0, 0.0)
    df['loss'] = -df.change.mask(df.change > 0, -0.0)

    gain_numpy = df.gain[window_length + 1:].to_numpy()
    loss_numpy = df.loss[window_length + 1:].to_numpy()
    df_gain_sum = np.nansum(df.gain.to_numpy()[:window_length + 1]) / window_length
    df_loss_sum = np.nansum(df.loss.to_numpy()[:window_length + 1]) / window_length

    df['avg_gain'] = rma(gain_numpy, window_length, df_gain_sum)
    df['avg_loss'] = rma(loss_numpy, window_length, df_loss_sum)
    df['rs'] = df.avg_gain / df.avg_loss
    df['rsi_14'] = 100 - (100 / (1 + df.rs))

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
                'chart_date': row['chart_date'],
                'volume': row['volume']
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

        volumes = []
        for row in line:
            volumes.append(row['volume'])

        # print(numpy.average(volumes), len(line))

    # print("average days a stock is above the (200,150,50) MA is = ", numpy.average(total_days))
    # print(stats.mode(total_days)[1])
    # print(total_days)
    # print(len(total_days))

    print(df)

    if with_chart:
        plt.plot(df['close'], 'k-', label='Original')
        plt.plot(df['sma_50'], 'g-', label='50 Day MA')
        plt.plot(df['sma_150'], 'r-', label='150 Day MA')
        plt.plot(df['sma_200'], 'b-', label='200 Day MA')

        plt.ylabel('Price')
        plt.xlabel('Date')

        plt.grid(linestyle=':')

        plt.fill_between(df['sma_50'].index, 0, df['sma_50'], color='g', alpha=0.1)
        plt.fill_between(df['sma_150'].index, 0, df['sma_150'], color='r', alpha=0.1)
        plt.fill_between(df['sma_200'].index, 0, df['sma_200'], color='b', alpha=0.1)
        # plt.bar(df['chart_date'], df['volume'], width=15, color='darkgrey')
        plt.legend(loc='upper left')
        plt.show()

    if len(total_days):
        average_days = np.average(total_days)
        mode = stats.mode(total_days, keepdims=False)
        return {'average': average_days, 'mode': mode[0], 'count': mode[1]}
    return False


def update_chart_data(chunked):
    connection = test_connection()
    cursor = connection.cursor()
    sql = "UPDATE chart_data SET rsi_14 = %s, sma_200 = %s, sma_150 = %s, sma_50 = %s WHERE id = %s "
    values = []
    for row in chunked.itertuples():
        rsi_14 = row.rsi_14
        if math.isnan(row.rsi_14):
            rsi_14 = 0
        values.append((
            rsi_14,
            row.sma_200,
            row.sma_150,
            row.sma_50,
            row.id
        ))
    cursor.executemany(sql, values)
    connection.commit()


def compute_screener(company_id):
    redis_conn = Redis('localhost', 6379)
    q = Queue(connection=redis_conn)
    db_connection_str = 'mysql+pymysql://root@localhost/ph_stock_scraper'
    db_connection = create_engine(db_connection_str)
    sql = 'SELECT * FROM chart_data WHERE company_id = {0} ORDER BY chart_date ASC'.format(company_id)
    df = pd.read_sql_query(sql=sql, con=db_connection)

    # print(df[])

    # print(query)
    #
    # df = query['close'].to_frame()
    #
    # print(df)

    # df['id'] = query['id']
    df['sma_200'] = df['close'].rolling(200).mean()
    df['sma_150'] = df['close'].rolling(150).mean()
    df['sma_50'] = df['close'].rolling(50).mean()

    print(df)

    # df['chart_date'] = pd.to_datetime(query['chart_date'])
    # df['volume'] = query['volume']
    # df['average_above'] = False
    # df = df.sort_values(by='chart_date')
    # df = df.set_index(df['chart_date'])
    # df.dropna(inplace=True)
    #
    window_length = 14
    df['change'] = df['close'].diff()
    df['gain'] = df.change.mask(df.change < 0, 0.0)
    df['loss'] = -df.change.mask(df.change > 0, -0.0)
    gain_numpy = df.gain[window_length + 1:].to_numpy()
    loss_numpy = df.loss[window_length + 1:].to_numpy()
    df_gain_sum = np.nansum(df.gain.to_numpy()[:window_length + 1]) / window_length
    df_loss_sum = np.nansum(df.loss.to_numpy()[:window_length + 1]) / window_length
    df['avg_gain'] = rma(gain_numpy, window_length, df_gain_sum)
    df['avg_loss'] = rma(loss_numpy, window_length, df_loss_sum)
    df['rs'] = df.avg_gain / df.avg_loss
    df['rsi_14'] = 100 - (100 / (1 + df.rs))

    n = 1000
    list_df = [df[i:i + n] for i in range(0, df.shape[0], n)]

    for chunked in list_df:
        q.enqueue(
            update_chart_data,
            chunked=chunked
        )
    #
    return False
