from sqlalchemy import create_engine, Column, Integer, String, JSON, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class Block(Base):
    _tablename_ = 'blocks'
    id = Column(Integer, primary_key=True)
    index = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow)
    transactions = Column(JSON)
    proof = Column(Integer)
    previous_hash = Column(String(64))

engine = create_engine('sqlite:///blockchain.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
