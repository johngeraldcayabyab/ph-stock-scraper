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
    'pageNo': 2,  # total pages range
    'sortType': '',
    'dateSortType': 'DESC',
    'cmpySortType': 'ASC',
    'symbolSortType': 'ASC',
    'companyId': '',
    'keyword': '',
    'sector': 'ALL',
    'subsector': 'ALL'
})

soup = BeautifulSoup(companyList.text, 'html.parser')
tbody = soup.find_all("tbody")

for body in tbody:
    rows = body.find_all("tr")
    for row in rows:
        columns = row.find_all("td")
        cm_detail = columns[0].find('a')['onclick'].replace('cmDetail(', '').replace(');return false;', '').split(',')
        name = columns[0].find('a').contents[0]
        symbol = columns[1].find('a').contents[0]
        cmpy_id = cm_detail[0].replace("'", '')
        security_id = cm_detail[1].replace("'", '')

        print(name, symbol, cmpy_id, security_id)

        # for cm in cm_detail:
        #     cmpy_id = cm[0]
        #     security_id = cm[1]

        # print(cm_detail)
        # name = columns[0].content
        # print(columns[0].find('a').contents[0])

    # td = body

    # for td in
    # print(tr)

# print(pages)

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
