import datetime
import requests
from db import test_connection
from utils import date_today, yesterday


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
    val = []
    for data in chart_data:
        f = '%b %d, %Y %H:%M:%S'
        open_price = data['OPEN']
        close = data['CLOSE']
        high = data['HIGH']
        low = data['LOW']
        volume = data['VALUE']
        chart_date = datetime.datetime.strptime(data['CHART_DATE'], f)
        val.append((open_price, close, high, low, volume, chart_date, company_id))
    sql = "INSERT INTO chart_data (open, close, high, low, volume, chart_date, company_id) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    cursor.executemany(sql, val)
    connection.commit()


# 2 GO Group
print(yesterday())
scrap_and_insert_chart_data(22, 609, 532, "05-01-2023", yesterday())
