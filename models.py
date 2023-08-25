from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Text, func

engine = create_engine("postgresql://app:1234@127.0.0.1:5431/adv")
Session = sessionmaker(bind=engine)
Base = declarative_base(bind=engine)


class Advertisement(Base):
    __tablename__ = "advs_list"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    owner = Column(String, nullable=False)


Base.metadata.create_all()
