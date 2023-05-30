import datetime
import requests
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
    values = []
    for data in chart_data:
        f = '%b %d, %Y %H:%M:%S'
        open_price = data['OPEN']
        close = data['CLOSE']
        high = data['HIGH']
        low = data['LOW']
        volume = data['VALUE']
        chart_date = datetime.datetime.strptime(data['CHART_DATE'], f)
        uuid = int(company_id + chart_date.timestamp())
        values.append((uuid, open_price, close, high, low, volume, chart_date, company_id))
    unique_values = list(set(map(tuple, values)))
    sql = "INSERT INTO chart_data (uuid, open, close, high, low, volume, chart_date, company_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.executemany(sql, unique_values)
    connection.commit()
