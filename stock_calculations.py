import math

import pandas as pd
from redis import Redis
from rq import Queue
from sqlalchemy import create_engine

from db import test_connection
from utils import chunk_df


def update_chart_data_sma(chunked):
    connection = test_connection()
    cursor = connection.cursor()
    sql = "UPDATE chart_data SET sma_200 = %s, sma_150 = %s, sma_50 = %s WHERE id = %s "
    values = []
    for row in chunked.itertuples():
        sma_200 = row.sma_200
        sma_150 = row.sma_150
        sma_50 = row.sma_50
        if math.isnan(sma_200):
            sma_200 = None
        if math.isnan(sma_150):
            sma_150 = None
        if math.isnan(sma_50):
            sma_50 = None
        values.append((
            sma_200,
            sma_150,
            sma_50,
            row.id
        ))
    cursor.executemany(sql, values)
    connection.commit()


def update_chart_data_rsi(chunked):
    connection = test_connection()
    cursor = connection.cursor()
    sql = "UPDATE chart_data SET rsi_14 = %s WHERE id = %s "
    values = []
    for row in chunked.itertuples():
        rsi_14 = row.rsi_14
        if math.isnan(rsi_14):
            rsi_14 = None
        values.append((
            rsi_14,
            row.id
        ))
    cursor.executemany(sql, values)
    connection.commit()


def calculate_rsi(company_id):
    redis_conn = Redis('localhost', 6379)
    q = Queue(connection=redis_conn, name='update_chart_data_rsi')
    db_connection_str = 'mysql+pymysql://root@localhost/ph_stock_scraper'
    db_connection = create_engine(db_connection_str)
    sql = 'SELECT * FROM chart_data WHERE company_id = {0} ORDER BY chart_date ASC'.format(company_id)
    pd.set_option('mode.chained_assignment', None)
    df = pd.read_sql_query(sql=sql, con=db_connection).set_index(['id', 'chart_date'])
    #

    df['close_diff'] = df['close'].diff()
    df['gain'] = df['close_diff'].clip(lower=0).round(2)
    df['loss'] = df['close_diff'].clip(upper=0).abs().round(2)

    window_length = 14
    gain_rolling = df['gain'].rolling(window=window_length, min_periods=window_length)
    loss_rolling = df['loss'].rolling(window=window_length, min_periods=window_length)
    avg_gain_rolling = gain_rolling.mean()
    avg_loss_rolling = loss_rolling.mean()
    df['avg_gain'] = avg_gain_rolling[:window_length + 1].fillna(0)
    df['avg_loss'] = avg_loss_rolling[:window_length + 1].fillna(0)

    # Get WMS averages
    # Average Gains
    for i, row in enumerate(df['avg_gain'].iloc[window_length + 1:]):
        df['avg_gain'].iloc[i + window_length + 1] = (df['avg_gain'].iloc[i + window_length] * (window_length - 1) +
                                                      df['gain'].iloc[i + window_length + 1]) / window_length
    # Average Losses
    for i, row in enumerate(df['avg_loss'].iloc[window_length + 1:]):
        df['avg_loss'].iloc[i + window_length + 1] = (df['avg_loss'].iloc[i + window_length] * (window_length - 1) +
                                                      df['loss'].iloc[i + window_length + 1]) / window_length

    df['rs'] = df['avg_gain'] / df['avg_loss']
    df['rsi_14'] = 100 - (100 / (1.0 + df['rs']))

    df = df.reset_index()

    list_df = chunk_df(df, 1000)

    for chunked in list_df:
        q.enqueue(
            update_chart_data_rsi,
            chunked=chunked
        )


def calculate_sma(company_id):
    redis_conn = Redis('localhost', 6379)
    q = Queue(connection=redis_conn, name='update_chart_data_sma')
    db_connection_str = 'mysql+pymysql://root@localhost/ph_stock_scraper'
    db_connection = create_engine(db_connection_str)
    sql = 'SELECT * FROM chart_data WHERE company_id = {0} ORDER BY chart_date ASC'.format(company_id)
    pd.set_option('mode.chained_assignment', None)
    df = pd.read_sql_query(sql=sql, con=db_connection)
    df['sma_200'] = df['close'].rolling(200).mean()
    df['sma_150'] = df['close'].rolling(150).mean()
    df['sma_50'] = df['close'].rolling(50).mean()
    list_df = chunk_df(df, 1000)
    for chunked in list_df:
        q.enqueue(
            update_chart_data_sma,
            chunked=chunked
        )
    return False
