import mysql.connector
import requests
import datetime
from datetime import date

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="ph_stock_scraper"
)

cursor = connection.cursor()
cursor.execute("SELECT * FROM companies")
companies = cursor.fetchall()

for company in companies:
    cmpy_id = company[1]
    security_id = company[2]
    listing_date = company[5].strftime("%Y-%m-%d")
    response = requests.post('https://edge.pse.com.ph/common/DisclosureCht.ax', json={
        "cmpy_id": cmpy_id,
        "security_id": security_id,
        "startDate": listing_date,
        "endDate": date.today()
    }, headers={
        'Content-type': 'application/json',
        'Accept': 'text/plain'
    })
    chartData = response.json()['chartData']
    for data in chartData:
        cursor = connection.cursor()
        f = '%b %d, %Y %H:%M:%S'
        open_price = data['OPEN']
        close = data['CLOSE']
        high = data['HIGH']
        low = data['LOW']
        volume = data['VALUE']
        chart_date = datetime.datetime.strptime(data['CHART_DATE'], f)
        sql = "INSERT INTO chart_data (open, close, high, low, volume, chart_date) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (open_price, close, high, low, volume, chart_date)
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
