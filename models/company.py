from sqlalchemy import Column, Integer, DateTime, TIMESTAMP, String
from sqlalchemy.orm import relationship, declarative_base, sessionmaker
import sqlalchemy as db

engine = db.create_engine('mysql+pymysql://root@localhost/ph_stock_scraper')

# from models.chart_data import ChartData

Base = declarative_base()


class Company(Base):
    __tablename__ = 'companies'
    id = Column(Integer, primary_key=True)
    cmpy_id = Column(Integer)
    security_id = Column(Integer)
    name = Column(String)
    symbol = Column(String)
    listing_date = Column(DateTime)
    sector_id = Column(Integer)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)
    # chart_data = relationship(ChartData)

    def get_all(self):
        Session = sessionmaker(bind=engine)
        session = Session()
        result = session.query(Company).filter(Company.id == 288)

        for row in result:
            print(row.name)
