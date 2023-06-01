import os
from dotenv import load_dotenv
import mysql.connector

load_dotenv()

DB_HOST = os.getenv('DB_HOST')
DB_DATABASE = os.getenv('DB_DATABASE')
DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')


class Db:
    def __init__(self):
        pass
        self.connection = self.test_connection()
        self.cursor = self.connection.cursor()

    def connection(self):
        return mysql.connector.connect(
            host=DB_HOST,
            database=DB_DATABASE,
            user=DB_USERNAME,
            password=DB_PASSWORD,
        )

    def test_connection(with_db=True):
        if with_db:
            return mysql.connector.connect(
                host=DB_HOST,
                database=DB_DATABASE,
                user=DB_USERNAME,
                password=DB_PASSWORD,
            )
        return mysql.connector.connect(
            host=DB_HOST,
            user=DB_USERNAME,
            password=DB_PASSWORD
        )


def connection():
    return mysql.connector.connect(
        host=DB_HOST,
        database=DB_DATABASE,
        user=DB_USERNAME,
        password=DB_PASSWORD,
    )


def test_connection(with_db=True):
    if with_db:
        return mysql.connector.connect(
            host=DB_HOST,
            database=DB_DATABASE,
            user=DB_USERNAME,
            password=DB_PASSWORD,
        )
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USERNAME,
        password=DB_PASSWORD
    )
