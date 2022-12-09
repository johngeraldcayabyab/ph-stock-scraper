import mysql.connector

dbConnection = mysql.connector.connect(
    host="localhost",
    user="root",
    password=""
)

cursor = dbConnection.cursor()

cursor.execute("SHOW DATABASES")

isDbExist = False

for database in cursor:
    if "ph_stock_scraper" in database:
        isDbExist = True

if isDbExist != True:
    cursor.execute("CREATE DATABASE ph_stock_scraper")
    dbConnection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="ph_stock_scraper"
    )
    cursor = dbConnection.cursor()
    cursor.execute("CREATE TABLE sectors (id INT AUTO_INCREMENT PRIMARY KEY, cd_id VARCHAR(255), cd_name VARCHAR(255))")
