import datetime

import requests
from bs4 import BeautifulSoup

from db import test_connection
from utils import date_today


def scrap_and_insert_chart_data(company_id, cmpy_id, security_id, start_date=date_today(), end_date=date_today()):
    connection = test_connection()
    cursor = connection.cursor()
    response = requests.post('https://edge.pse.com.ph/common/DisclosureCht.ax', json={
        "cmpy_id": cmpy_id,
        "security_id": security_id,
        "startDate": start_date,
        "endDate": end_date
    }, headers={
        'Content-type': 'application/json',
        'Accept': 'application/json, text/javascript, */*; q=0.01'
    })
    chart_data = response.json()['chartData']
    for data in chart_data:
        f = '%b %d, %Y %H:%M:%S'
        open_price = data['OPEN']
        close = data['CLOSE']
        high = data['HIGH']
        low = data['LOW']
        volume = data['VALUE']
        chart_date = datetime.datetime.strptime(data['CHART_DATE'], f)
        sql = "INSERT INTO chart_data (open, close, high, low, volume, chart_date, company_id) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        val = (open_price, close, high, low, volume, chart_date, company_id)
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
        page_no = i + 1
        companies = requests.post('https://edge.pse.com.ph/companyDirectory/search.ax', data={
            'pageNo': page_no,
            'sortType': '',
            'dateSortType': 'DESC',
            'cmpySortType': 'ASC',
            'symbolSortType': 'ASC',
            'companyId': '',
            'keyword': '',
            'sector': 'ALL',
            'subsector': 'ALL'
        }, headers={
            'accept': '*/*',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8'
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
                # sql = "SELECT cmpy_id, COUNT(*) FROM companies WHERE cmpy_id = %s AND security_id = %s GROUP BY cmpy_id, security_id"
                # val = (cmpy_id, security_id,)
                # cursor.execute(sql, val)
                # cursor.fetchall()
                # row_count = cursor.rowcount
                # if row_count == 0:
                #     print("It Does Not Exist")
                sql = "INSERT INTO companies (name, symbol, cmpy_id, security_id, listing_date) VALUES (%s, %s, %s, %s, %s)"
                val = (name, symbol, cmpy_id, security_id, listing_date)
                cursor.execute(sql, val)

    connection.commit()

# print(companies)

# def add_one_day(date):
#     for i in range(5):
#         date += datetime.timedelta(days=1)
#         return date
#
#
# # getAllDays
#
# listing_date = companies[0][5]
# delta = date.today() - listing_date.date()
# days = delta.days
#
# for day in range(days):
#     day += 1

# print(days)

# for

# for

# for company in companies:
#     print(company[5], add_one_day(company[5]), date.today().strftime("%Y-%m-%d %H:%M:%S"))

# response = requests.post('https://edge.pse.com.ph/common/DisclosureCht.ax', json={
#     "cmpy_id": "29",
#     "security_id": "146",
#     "startDate": "01-01-1995",
#     "endDate": "12-12-2022"
# }, headers={
#     'Content-type': 'application/json',
#     'Accept': 'text/plain'
# })
#
# chartData = response.json()['chartData']

# print(len(chartData))

# #
# for data in chartData:
#     cursor = connection.cursor()
#     f = '%b %d, %Y %H:%M:%S'
#     open_price = data['OPEN']
#     close = data['CLOSE']
#     high = data['HIGH']
#     low = data['LOW']
#     volume = data['VALUE']
#     chart_date = datetime.datetime.strptime(data['CHART_DATE'], f)
#     sql = "INSERT INTO chart_data (open, close, high, low, volume, chart_date) VALUES (%s, %s, %s, %s, %s, %s)"
#     val = (open_price, close, high, low, volume, chart_date)
#     cursor.execute(sql, val)
#     connection.commit()
