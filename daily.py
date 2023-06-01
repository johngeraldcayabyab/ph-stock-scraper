from redis import Redis
from rq import Queue

from chart_data_scraper import scrap_and_insert_chart_data
from companies import Company
from scanner import minervini_scanner
from stock_calculations import calculate_rsi, calculate_sma
from utils import yesterday, date_today


def get_all_chart_data(start_date=date_today(), end_date=date_today()):
    redis_conn = Redis('localhost', 6379)
    scraper_queue = Queue(connection=redis_conn, name='scrap_and_insert_chart_data')
    companies = Company().get_all_companies()
    for company in companies:
        scraper_queue.enqueue(
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

    companies = Company().get_all_companies()
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


get_all_chart_data(start_date="05-01-2023", end_date=date_today())

# calculate_rsi(169)
# calculate_sma(169)

# override_date = '12-15-2022'
# insert_companies()
# get_all_chart_data('12-23-2022', yesterday())
# get_all_chart_data('01-05-2023', '05-18-2023')
# minervini_scanner(22, with_chart=True)
# print((date.today() - timedelta(days=1)).strftime("%m-%d-%Y"))

# compute_all_chart_data()
