import requests
from redis import Redis
from rq import Queue

from chart_data_scraper import scrap_and_insert_chart_data, insert_companies
from db import test_connection


def initialize_database():
    connection = test_connection(with_db=False)
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
