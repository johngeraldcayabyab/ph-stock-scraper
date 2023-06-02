import sqlalchemy as db

engine = db.create_engine('mysql+pymysql://root@localhost/ph_stock_scraper')
connection = engine.connect()
metadata = db.MetaData()
sectors = db.Table('sectors', metadata, autoload=True, autoload_with=engine)
print(sectors.columns.keys())
query = db.select([sectors])
print(query)
ResultProxy = connection.execute(query)
ResultSet = ResultProxy.fetchall()
print(ResultSet)
