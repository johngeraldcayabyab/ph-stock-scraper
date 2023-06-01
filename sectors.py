import requests
from db import test_connection


class Sector:
    def __init__(self):
        self.connection = test_connection()
        self.cursor = self.connection.cursor()

    def get_sectors(self):
        return requests.post('https://edge.pse.com.ph/common/chgSector.ax', json={"idxId": ""}, headers={
            'Content-type': 'application/json',
            'Accept': 'text/plain'
        }).json()

    def create_or_update(self, fetched_sectors):
        current_sectors = self.get_current_sectors()
        val = []
        for fetched_sector in fetched_sectors:
            fetched_sector_id = fetched_sector['cdId']
            if self.is_new_sector(fetched_sector_id, current_sectors):
                val.append((fetched_sector['cdId'], fetched_sector['cdNm']))
        val.append(("Undefined", "Undefined"))
        sql = "INSERT INTO sectors (cd_id, cd_name) VALUES (%s, %s)"
        if len(val):
            self.cursor.executemany(sql, val)
            self.connection.commit()

    def get_sectors_and_create_or_update(self):
        sectors = self.get_sectors()
        self.create_or_update(sectors)

    def is_new_sector(self, fetched_sector_id, current_sectors):
        for current_sector in current_sectors:
            current_sector_id = current_sector[1]
            if fetched_sector_id == current_sector_id:
                return False
        return True

    def get_current_sectors(self):
        self.cursor.execute("SELECT id, cd_id FROM sectors")
        return self.cursor.fetchall()

    def get_sector_id_by_name(self, sectors, sector_name):
        for sector in sectors:
            if (sector[1] == sector_name):
                return sector[0]
        self.cursor.execute("SELECT id FROM sectors where cd_id = 'Undefined'")
        undefined_sector = self.cursor.fetchall()
        return undefined_sector[0][0]
