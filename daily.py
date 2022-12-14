# Should make a daily scraper to get all companies, download all data if company is new

def get_new_companies():
    cursor.execute(
        "SELECT Name, COUNT(*) FROM Item_Info WHERE Name = %s GROUP BY Name",
        (item_name,)
    )
    # gets the number of rows affected by the command executed
    row_count = cursor.rowcount
    print("number of affected rows: {}".format(row_count))
    if row_count == 0:
        print("It Does Not Exist")
