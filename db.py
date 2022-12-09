import mysql.connector
import requests
from bs4 import BeautifulSoup

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password=""
)

cursor = connection.cursor()

cursor.execute("SHOW DATABASES")

is_db_exist = False

for database in cursor:
    if "ph_stock_scraper" in database:
        is_db_exist = True

if is_db_exist:
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="ph_stock_scraper"
    )

else:
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE ph_stock_scraper")
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="ph_stock_scraper"
    )
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE sectors (id INT AUTO_INCREMENT PRIMARY KEY, cd_id VARCHAR(255), cd_name VARCHAR(255))")
    cursor.execute(
        "CREATE TABLE companies ("
        " id INT AUTO_INCREMENT PRIMARY KEY,"
        " cmpy_id INT, security_id INT,"
        " name VARCHAR(255),"
        " symbol VARCHAR(255)"
        ")")

headers = {
    'Content-type': 'application/json',
    'Accept': 'text/plain'
}


def insert_sectors():
    sectors = requests.post('https://edge.pse.com.ph/common/chgSector.ax', json={"idxId": ""}, headers=headers)

    for sector in sectors.json():
        sql = "INSERT INTO sectors (cd_id, cd_name) VALUES (%s, %s)"
        val = (sector['cdId'], sector['cdNm'])
        cursor.execute(sql, val)


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

                sql = "INSERT INTO companies (name, symbol, cmpy_id, security_id) VALUES (%s, %s, %s, %s)"
                val = (name, symbol, cmpy_id, security_id)
                cursor.execute(sql, val)


insert_sectors()
insert_companies()
connection.commit()
