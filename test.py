import requests

headers = {
    'Content-type': 'application/json',
    'Accept': 'text/plain'
}

payload = {
    "cmpy_id": "233",
    "security_id": "140",
    "startDate": "12-02-2021",
    "endDate": "12-02-2022"
}

# response = requests.post('https://edge.pse.com.ph/common/DisclosureCht.ax', json=payload, headers=headers)
# print(response.json())

# cmDetail('13','234')
# cmpy_id = 13
# security_id = 140
# companyList = requests.post('https://edge.pse.com.ph/companyDirectory/search.ax')
# print(companyList.text)


# sectors list
sectorList = requests.post('https://edge.pse.com.ph/common/chgSector.ax', json={"idxId": ""}, headers=headers)
print(sectorList.json())
