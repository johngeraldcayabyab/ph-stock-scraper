import requests
from bs4 import BeautifulSoup

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
companyList = requests.post('https://edge.pse.com.ph/companyDirectory/search.ax', json={
    'companyId': '',
    'keyword': '',
    'sector': 'ALL',
    'subsector': 'ALL'
})

soup = BeautifulSoup(companyList.text, 'html.parser')

pages = soup.find_all("div", class_="paging")[0].contents

total_pages = 0

for page in pages:
    if page.name == 'span':
        total_pages += 1


print(total_pages)

# print(soup.find_all("div", class_="paging")[0].contents[0])

# print(companyList.text)


# companyList = requests.post('', json={
#     'pageNo': 2,
#     'sortType': '',
#     'dateSortType': 'DESC',
#     'cmpySortType': 'ASC',
#     'symbolSortType': 'ASC',
#     'companyId': '',
#     'keyword': '',
#     'sector': 'ALL',
#     'subsector': 'ALL'
# })

# sectors list
# sectors = requests.post('https://edge.pse.com.ph/common/chgSector.ax', json={"idxId": ""}, headers=headers)
#
# for sector in sectors.json():
#     print(sector)


# print(sectorList.json())
