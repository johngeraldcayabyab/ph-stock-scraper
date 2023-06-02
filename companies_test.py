import datetime

import requests
from bs4 import BeautifulSoup
from db import Db
from sectors import Sector


class CompanyTest(Db):
    def insert_companies(self):
        total_pages = self.get_total_pages()
        val = []
        sectors = Sector().get_current_sectors()
        current_company_symbols = self.get_current_company_symbols()
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
                    name = columns[0].find('a').contents[0].strip()
                    fetched_symbol = columns[1].find('a').contents[0].strip()
                    sector_name = columns[3].contents[0].strip()
                    sector_id = Sector().get_sector_id_by_name(sectors, sector_name)
                    cmpy_id = cm_detail[0].replace("'", '').strip()
                    security_id = cm_detail[1].replace("'", '').strip()
                    listing_date = columns[4].contents[0].strip()
                    f = '%b %d, %Y'
                    listing_date = datetime.datetime.strptime(listing_date, f)
                    if self.is_new_company(fetched_symbol, current_company_symbols):
                        val.append((name, fetched_symbol, cmpy_id, security_id, listing_date, sector_id))

        if len(val):
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

    def is_new_company(self, fetched_company_symbol, company_symbols):
        for company_symbol in company_symbols:
            current_company_symbol = company_symbol[0]
            if fetched_company_symbol == current_company_symbol:
                return False
        return True

    def get_current_company_symbols(self):
        self.cursor.execute("SELECT symbol FROM companies")
        return self.cursor.fetchall()

    def get_all_companies(self):
        self.cursor.execute("SELECT * FROM companies")
        return self.cursor.fetchall()
