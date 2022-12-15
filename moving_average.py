from redis import Redis
from rq import Queue

from db import test_connection
from stock_calculations import calculate_close_above_200_150_50_MA


def save_200_150_50_MA_average():
    connection = test_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM companies")
    companies = cursor.fetchall()
    for company in companies:
        results = calculate_close_above_200_150_50_MA(str(company[0]))
        if results:
            sql = "INSERT INTO average_up_days (days, mode, count, company_id) VALUES (%s, %s, %s, %s)"
            val = (int(results['average']), int(results['mode']), int(results['count']), company[0])
            cursor.execute(sql, val)
        print(results, company[0])
    connection.commit()


save_200_150_50_MA_average()
