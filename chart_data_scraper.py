import datetime
import requests
from db import Db, test_connection
from utils import date_today


def scrap_and_insert_chart_data(company_id, cmpy_id, security_id, start_date=date_today(),
                                end_date=date_today()):
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
    uuidsList = get_all_uuid(company_id)
    uuids = []
    for uuidList in uuidsList:
        uuids.append(uuidList[0])

    print(chart_data)

    for data in chart_data:
        f = '%b %d, %Y %H:%M:%S'
        chart_date = datetime.datetime.strptime(data['CHART_DATE'], f)
        uuid = int(company_id + chart_date.timestamp())
        if uuid in uuids:
            continue
        open_price = data['OPEN']
        close = data['CLOSE']
        high = data['HIGH']
        low = data['LOW']
        volume = data['VALUE']
        values.append((uuid, open_price, close, high, low, volume, chart_date, company_id))
    unique_values = list(set(map(tuple, values)))
    sql = "INSERT INTO chart_data (uuid, open, close, high, low, volume, chart_date, company_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.executemany(sql, unique_values)
    connection.commit()


def get_all_uuid(company_id):
    connection = test_connection()
    cursor = connection.cursor()
    sql = 'SELECT uuid FROM chart_data WHERE company_id = {0}'.format(company_id)
    cursor.execute(sql)
    return cursor.fetchall()
