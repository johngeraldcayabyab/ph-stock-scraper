import requests
from db import test_connection


class Sector:
    def get_sectors(self):
        return requests.post('https://edge.pse.com.ph/common/chgSector.ax', json={"idxId": ""}, headers={
            'Content-type': 'application/json',
            'Accept': 'text/plain'
        }).json()

    def create_or_update(self, fetched_sectors):
        connection = test_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM sectors")
        current_sectors = cursor.fetchall()
        val = []
        for fetched_sector in fetched_sectors:
            fetched_sector_id = fetched_sector['cdId']
            if self.is_new_sector(fetched_sector_id, current_sectors):
                val.append((fetched_sector['cdId'], fetched_sector['cdNm']))
        sql = "INSERT INTO sectors (cd_id, cd_name) VALUES (%s, %s)"
        cursor.executemany(sql, val)
        connection.commit()

    def get_sectors_and_create_or_update(self):
        sectors = self.get_sectors()
        self.create_or_update(sectors)

    def is_new_sector(self, fetched_sector_id, current_sectors):
        for current_sector in current_sectors:
            current_sector_id = current_sector[1]
            if fetched_sector_id == current_sector_id:
                return False
        return True
