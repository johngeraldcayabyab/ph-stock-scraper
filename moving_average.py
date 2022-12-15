from redis import Redis
from rq import Queue

from db import test_connection
from stock_calculations import calculate_close_above_200_150_50_MA


def save_200_150_50_MA_average():
    # redis_conn = Redis('localhost', 6379)
    # q = Queue(connection=redis_conn)
    connection = test_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM companies")
    companies = cursor.fetchall()
    for company in companies:
        # company_id = str(company[0])
        # q.enqueue(
        #     calculate_close_above_200_150_50_MA,
        #     company_id=company_id,
        # )
        results = calculate_close_above_200_150_50_MA(str(company[0]))
        print(results, company[0])
        # if results['average']:
        # if(results['average'], results['mode'])
        # print(results)
        sql = "INSERT INTO average_up_days (days, mode, count, company_id) VALUES (%s, %s, %s, %s)"
        val = (int(results['average']), int(results['mode']), int(results['count']), company[0])
        cursor.execute(sql, val)
    connection.commit()


save_200_150_50_MA_average()
# calculate_close_above_200_150_50_MA("10")
