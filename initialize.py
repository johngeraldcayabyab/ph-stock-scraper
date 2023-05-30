import requests
from redis import Redis
from rq import Queue
from sectors import Sector
from companies import Company

from db import test_connection


class Initializer:
    def initialize(self):
        self.initialize_database()
        self.initialize_tables()
        Sector().get_sectors_and_create_or_update()
        Company().insert_companies()
        print('initialization done')

    def initialize_database(self):
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

    def initialize_tables(self):
        connection = test_connection()
        cursor = connection.cursor()
        cursor.execute(
            " CREATE TABLE sectors ("
            " id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,"
            " cd_id VARCHAR(255),"
            " cd_name VARCHAR(255),"
            " created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,"
            " updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP"
            ")"
        )
        cursor.execute(
            " CREATE TABLE companies ("
            " id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,"
            " cmpy_id INT,"
            " security_id INT,"
            " name VARCHAR(255),"
            " symbol VARCHAR(255),"
            " listing_date DATETIME,"
            " sector_id INT UNSIGNED,"
            " CONSTRAINT fk_sectors FOREIGN KEY (sector_id) REFERENCES sectors(ID),"
            " created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,"
            " updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP"
            ")"
        )
        cursor.execute(
            " CREATE TABLE chart_data ("
            " id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,"
            " uuid INT UNSIGNED,"
            " open DECIMAL(13,4),"
            " close DECIMAL(13,4),"
            " high DECIMAL(13,4),"
            " low DECIMAL(13,4),"
            " volume DECIMAL(19,4),"
            " sma_50 DECIMAL(13,4) NULL,"
            " sma_150 DECIMAL(13,4) NULL,"
            " sma_200 DECIMAL(13,4) NULL,"
            " rsi_14 DECIMAL(13,4) NULL,"
            " chart_date DATETIME,"
            " company_id INT UNSIGNED,"
            " CONSTRAINT fk_companies FOREIGN KEY (company_id) REFERENCES companies(ID),"
            " created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,"
            " updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,"
            " UNIQUE (uuid)"
            ")"
        )
        connection.commit()


# def get_all_chart_data():
#     redis_conn = Redis('localhost', 6379)
#     q = Queue(connection=redis_conn)
#
#     connection = test_connection()
#     cursor = connection.cursor()
#     cursor.execute("SELECT * FROM companies")
#     companies = cursor.fetchall()
#
#     for company in companies:
#         q.enqueue(
#             scrap_and_insert_chart_data,
#             cmpy_id=company[1],
#             security_id=company[2],
#             start_date=company[5].strftime("%m-%d-%Y"),
#             company_id=company[0]
#         )


# sectorClass = Sector()
# sectorClass.get_sectors_and_create_or_update()
# insert_companies()
# get_all_chart_data()

Initializer().initialize()
