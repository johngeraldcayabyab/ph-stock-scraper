from sqlalchemy import Column, Integer, Float, DateTime, TIMESTAMP, ForeignKey
from sqlalchemy.ext.declarative import DeclarativeMeta
from models.company import Company


class ChartData(DeclarativeMeta):
    __tablename__ = 'chart_data'
    id = Column(Integer, primary_key=True)
    uuid = Column(Integer)
    open = Column(Float)
    close = Column(Float)
    high = Column(Float)
    low = Column(Float)
    volume = Column(Float)
    sma_50 = Column(Float)
    sma_150 = Column(Float)
    sma_200 = Column(Float)
    rsi_14 = Column(Float)
    chart_date = Column(DateTime)
    company_id = Column(Integer, ForeignKey(Company.id))
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)
