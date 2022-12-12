import mysql.connector
import requests
import datetime

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="ph_stock_scraper"
)

cursor = connection.cursor()

# cursor.execute("SELECT * FROM companies")
#
# companies = cursor.fetchall()
#
# for company in companies:
#     print(company)


response = requests.post('https://edge.pse.com.ph/common/DisclosureCht.ax', json={
    "cmpy_id": "29",
    "security_id": "146",
    "startDate": "01-01-2021",
    "endDate": "12-31-2021"
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
    value = data['VALUE']
    chart_date = datetime.datetime.strptime(data['CHART_DATE'], f)
    sql = "INSERT INTO chart_data (open, close, high, low, value, chart_date) VALUES (%s, %s, %s, %s, %s, %s)"
    val = (open_price, close, high, low, value, chart_date)
    cursor.execute(sql, val)
    connection.commit()
