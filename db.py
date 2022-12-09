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

isDbExist = False

for database in cursor:
    if "ph_stock_scraper" in database:
        isDbExist = True

if isDbExist != True:
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
else:
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="ph_stock_scraper"
    )
    cursor = connection.cursor()

headers = {
    'Content-type': 'application/json',
    'Accept': 'text/plain'
}

sectors = requests.post('https://edge.pse.com.ph/common/chgSector.ax', json={"idxId": ""}, headers=headers)

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

    print(total_pages)
