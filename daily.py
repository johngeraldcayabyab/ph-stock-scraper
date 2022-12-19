from datetime import date, timedelta

from redis import Redis
from rq import Queue
from chart_data_scraper import scrap_and_insert_chart_data, insert_companies
from db import test_connection
from stock_calculations import minervini_scanner, compute_screener


def get_all_chart_data():
    redis_conn = Redis('localhost', 6379)
    q = Queue(connection=redis_conn)
    connection = test_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM companies")
    companies = cursor.fetchall()
    today = date.today().strftime("%m-%d-%Y")
    yesterday = (date.today() - timedelta(days=1)).strftime("%m-%d-%Y")
    for company in companies:
        q.enqueue(
            scrap_and_insert_chart_data,
            cmpy_id=company[1],
            security_id=company[2],
            listing_date=yesterday,
            company_id=company[0]
        )


def compute_all_chart_data():
    connection = test_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM companies")
    companies = cursor.fetchall()
    for company in companies:
        compute_screener(company_id=company[0])


# insert_companies()
# get_all_chart_data()
# minervini_scanner(159, with_chart=True)
# print((date.today() - timedelta(days=1)).strftime("%m-%d-%Y"))

compute_all_chart_data()
