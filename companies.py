import datetime
import requests
from bs4 import BeautifulSoup
from db import test_connection
from sectors import Sector


class Company:
    def __init__(self):
        self.connection = test_connection()
        self.cursor = self.connection.cursor()

    def insert_companies(self):
        total_pages = self.get_total_pages()
        val = []
        sectors = Sector().get_current_sectors()
        for i in range(total_pages):
            page_no = i + 1
            companies = requests.post('https://edge.pse.com.ph/companyDirectory/search.ax', data={
                'pageNo': page_no,
                'sortType': '',
                'dateSortType': 'DESC',
                'cmpySortType': 'ASC',
                'symbolSortType': 'ASC',
                'companyId': '',
                'keyword': '',
                'sector': 'ALL',
                'subsector': 'ALL'
            }, headers={
                'accept': '*/*',
                'content-type': 'application/x-www-form-urlencoded; charset=UTF-8'
            })
            soup = BeautifulSoup(companies.text, 'html.parser')
            t_body = soup.find_all("tbody")
            for body in t_body:
                rows = body.find_all("tr")
                for row in rows:
                    columns = row.find_all("td")
                    cm_detail = columns[0].find('a')['onclick'].replace('cmDetail(', '').replace(');return false;',
                                                                                                 '').split(
                        ',')
                    name = columns[0].find('a').contents[0]
                    symbol = columns[1].find('a').contents[0]
                    sector_name = columns[3].contents[0].strip()
                    sector_id = Sector().get_sector_id_by_name(sectors, sector_name)
                    cmpy_id = cm_detail[0].replace("'", '')
                    security_id = cm_detail[1].replace("'", '')
                    listing_date = columns[4].contents[0]
                    f = '%b %d, %Y'
                    listing_date = datetime.datetime.strptime(listing_date, f)
                    val.append((name, symbol, cmpy_id, security_id, listing_date, sector_id))
        sql = "INSERT INTO companies (name, symbol, cmpy_id, security_id, listing_date, sector_id) VALUES (%s, %s, %s, %s, %s, %s)"
        self.cursor.executemany(sql, val)
        self.connection.commit()

    def get_total_pages(self):
        company_list = requests.post('https://edge.pse.com.ph/companyDirectory/search.ax', json={
            'companyId': '',
            'keyword': '',
            'sector': 'ALL',
            'subsector': 'ALL'
        })
        soup = BeautifulSoup(company_list.text, 'html.parser')
        pages = soup.find_all("div", class_="paging")[0].contents
        total_pages = 0
        for page in pages:
            if page.name == 'span':
                total_pages += 1
        return total_pages
