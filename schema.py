from sqlalchemy import Column, Integer, Float, DateTime, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

Base = declarative_base()

class Plant(Base):
    __tablename__ = 'plants'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __repr__(self):
        return f'{self.name} ({self.id})'

class MMType(Base):
    __tablename__ = 'types'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    
    def __repr__(self):
        return f'{self.name} ({self.id})'


class Point(Base):
    __tablename__ = 'points'

    id = Column(Integer, primary_key=True)
    value = Column(Float)
    time = Column(DateTime, server_default=func.now())
    plant_id = Column(Integer, ForeignKey('plants.id'))
    type_id = Column(Integer, ForeignKey('types.id'))

    plant = relationship("Plant", back_populates="points")

Plant.points = relationship("Point", back_populates="plant")

