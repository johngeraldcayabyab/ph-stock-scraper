import requests
import datetime

response = requests.post('https://edge.pse.com.ph/common/DisclosureCht.ax', json={
    "cmpy_id": "29",
    "security_id": "146",
    "startDate": "05-15-2020",
    "endDate": "12-31-2021"
}, headers={
    'Content-type': 'application/json',
    'Accept': 'text/plain'
})
print(response.json()['chartData'])