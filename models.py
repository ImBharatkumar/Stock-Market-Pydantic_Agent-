from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Competitor(Base):
    __tablename__ = 'competitors'

    id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    name = Column(String, index=True)
    sector = Column(String)
    price_to_earning = Column(Float)
    market_share = Column(Float)

# Pydantic model for request/response validation
from pydantic import BaseModel

class CompetitorCreate(BaseModel):
    id :int
    name: str
    sector: str
    price_to_earning : float
    market_share: float

class CompetitorResponse(CompetitorCreate):
    id: int

    class Config:
        orm_mode = True