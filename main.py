<<<<<<< HEAD
import requests

response = requests.get('https://phisix-api4.appspot.com/stocks/BDO.2021-01-01.json')
=======
# import requests

import requests

# import requests
#
# response = requests.get(
#     'https://api.investing.com/api/financialdata/historical/102326?start-date=2021-01-01&end-date=2021-12-01&time-frame=Daily&add-missing-rows=false')
#
# print(response)
#
# # response = requests.get('https://phisix-api4.appspot.com/stocks/BDO.2021-01-01.json')
# # print(response)

payload = {
    "cmpy_id": "233",
    "security_id": "140",
    "startDate": "12-02-2021",
    "endDate": "12-02-2022"
}
response = requests.post('https://edge.pse.com.ph/common/DisclosureCht.ax', payload)
>>>>>>> bf2c97fa3304f6984a81d5a6a45ac6ab345bf988
print(response)