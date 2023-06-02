# import sqlalchemy as db
# from sqlalchemy.orm import sessionmaker
#
# from models.company import Company
#
# engine = db.create_engine('mysql+pymysql://root@localhost/ph_stock_scraper')
# # connection = engine.connect()
# # metadata = db.MetaData()
# # sectors = db.Table('sectors', metadata, autoload=True, autoload_with=engine)
# # print(sectors.columns.keys())
# # query = db.select([sectors])
# # print(query)
# # ResultProxy = connection.execute(query)
# # ResultSet = ResultProxy.fetchall()
# # print(ResultSet)
# #
# # Session = sessionmaker(bind=engine)
# # session = Session()
# # result = session.query(Company).filter(Company.id == 288)
# #
# # for row in result:
# #     print(row.name)
from models.company import Company

Company().get_all()
