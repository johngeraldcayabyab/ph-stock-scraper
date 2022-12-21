from redis import Redis
from rq import Queue

from chart_data_scraper import scrap_and_insert_chart_data, date_today
from db import test_connection
from stock_calculations import calculate_rsi, calculate_sma


def get_all_chart_data(start_date=date_today(), end_date=date_today()):
    redis_conn = Redis('localhost', 6379)
    q = Queue(connection=redis_conn)
    connection = test_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM companies")
    companies = cursor.fetchall()
    for company in companies:
        q.enqueue(
            scrap_and_insert_chart_data,
            cmpy_id=company[1],
            security_id=company[2],
            start_date=start_date,
            end_date=end_date,
            company_id=company[0]
        )


def compute_all_chart_data():
    redis_conn = Redis('localhost', 6379)
    rsi_queue = Queue(connection=redis_conn, name='calculate_rsi')
    sma_queue = Queue(connection=redis_conn, name='calculate_sma')
    connection = test_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM companies")
    companies = cursor.fetchall()
    for index, company in enumerate(companies):
        company_id = company[0]
        rsi_queue.enqueue(
            calculate_rsi,
            company_id=company_id,
        )
        sma_queue.enqueue(
            calculate_sma,
            company_id=company_id,
        )


# calculate_rsi(169)
# calculate_sma(169)

# override_date = '12-15-2022'
# insert_companies()
# get_all_chart_data(yesterday(), yesterday())
# minervini_scanner(159, with_chart=True)
# print((date.today() - timedelta(days=1)).strftime("%m-%d-%Y"))

compute_all_chart_data()
