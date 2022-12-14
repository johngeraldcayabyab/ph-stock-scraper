import datetime
import requests
from bs4 import BeautifulSoup
from rq import Queue
from redis import Redis
from chart_data_scraper import scrap_and_insert_chart_data
from db import test_connection


def initialize_database():
    connection = test_connection()
    cursor = connection.cursor()
    cursor.execute("SHOW DATABASES")
    is_db_exist = False
    for database in cursor:
        if "ph_stock_scraper" in database:
            is_db_exist = True
            break
    if is_db_exist:
        connection = test_connection()
        cursor = connection.cursor()
        cursor.execute("DROP DATABASE ph_stock_scraper")
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE ph_stock_scraper")
    connection.commit()


def create_tables():
    connection = test_connection()
    cursor = connection.cursor()
    cursor.execute(
        "CREATE TABLE sectors ("
        " id INT AUTO_INCREMENT PRIMARY KEY,"
        " cd_id VARCHAR(255),"
        " cd_name VARCHAR(255),"
        " created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP"
        ")")
    cursor.execute(
        "CREATE TABLE companies ("
        " id INT AUTO_INCREMENT PRIMARY KEY,"
        " cmpy_id INT,"
        " security_id INT,"
        " name VARCHAR(255),"
        " symbol VARCHAR(255),"
        " listing_date DATETIME,"
        " created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP"
        ")")
    cursor.execute(
        "CREATE TABLE chart_data ("
        " id INT AUTO_INCREMENT PRIMARY KEY,"
        " open DECIMAL(13,4),"
        " close DECIMAL(13,4),"
        " high DECIMAL(13,4),"
        " low DECIMAL(13,4),"
        " volume DECIMAL(19,4),"
        " chart_date DATETIME,"
        " company_id INT,"
        " CONSTRAINT fk_companies FOREIGN KEY (company_id) REFERENCES companies(ID),"
        " created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP"
        ")")
    connection.commit()


def insert_sectors():
    connection = test_connection()
    cursor = connection.cursor()
    sectors = requests.post('https://edge.pse.com.ph/common/chgSector.ax', json={"idxId": ""}, headers={
        'Content-type': 'application/json',
        'Accept': 'text/plain'
    })
    for sector in sectors.json():
        sql = "INSERT INTO sectors (cd_id, cd_name) VALUES (%s, %s)"
        val = (sector['cdId'], sector['cdNm'])
        cursor.execute(sql, val)
    connection.commit()


def get_total_pages():
    company_list = requests.post('https://edge.pse.com.ph/companyDirectory/search.ax', json={
        'companyId': '',
        'keyword': '',
        'sector': 'ALL',
        'subsector': 'ALL'
    })
    soup = BeautifulSoup(company_list.text, 'html.parser')
    pages = soup.find_all("div", class_="paging")[0].contents
    total_pages = 0
    for page in pages:
        if page.name == 'span':
            total_pages += 1
    return total_pages


def insert_companies():
    connection = test_connection()
    cursor = connection.cursor()
    for i in range(get_total_pages()):
        companies = requests.post('https://edge.pse.com.ph/companyDirectory/search.ax', json={
            'pageNo': i,
            'sortType': '',
            'dateSortType': 'DESC',
            'cmpySortType': 'ASC',
            'symbolSortType': 'ASC',
            'companyId': '',
            'keyword': '',
            'sector': 'ALL',
            'subsector': 'ALL'
        })
        soup = BeautifulSoup(companies.text, 'html.parser')
        t_body = soup.find_all("tbody")
        for body in t_body:
            rows = body.find_all("tr")
            for row in rows:
                columns = row.find_all("td")
                cm_detail = columns[0].find('a')['onclick'].replace('cmDetail(', '').replace(');return false;',
                                                                                             '').split(
                    ',')
                name = columns[0].find('a').contents[0]
                symbol = columns[1].find('a').contents[0]
                cmpy_id = cm_detail[0].replace("'", '')
                security_id = cm_detail[1].replace("'", '')
                listing_date = columns[4].contents[0]
                f = '%b %d, %Y'
                listing_date = datetime.datetime.strptime(listing_date, f)
                sql = "INSERT INTO companies (name, symbol, cmpy_id, security_id, listing_date) VALUES (%s, %s, %s, %s, %s)"
                val = (name, symbol, cmpy_id, security_id, listing_date)
                cursor.execute(sql, val)
    connection.commit()


def get_all_chart_data():
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


initialize_database()
create_tables()
insert_sectors()
insert_companies()
get_all_chart_data()

print('initialization done')
