import sqlalchemy

from sqlalchemy.orm import sessionmaker
import config
import schema

class DBConnection:
    def __init__(self):
        self.engine = sqlalchemy.create_engine('sqlite:///'+config.DB.path)
        self.session = sessionmaker(bind=self.engine)()

    def migrate(self):
        schema.Base.metadata.create_all(self.engine)

    def make_mm_type(self, name):
        mmtype = schema.MMType(name=name)
        self.session.add(mmtype)
        self.session.commit()

    def make_plant(self, name):
        plant = schema.Plant(name=name)
        self.session.add(plant)
        self.session.commit()

    def measure(self, value, plant_id, type_id):
        mm = schema.Point(value=value, plant_id=plant_id, type_id=type_id)
        self.session.add(mm)
        self.session.commit()
