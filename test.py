from rq import Queue
from redis import Redis

from chart_data_scraper import scrap_and_insert_chart_data
from db import test_connection

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
        listing_date=company[5].strftime("%m-%d-%Y"),
        company_id=company[0]
    )
