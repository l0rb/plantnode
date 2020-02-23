import argparse

import sqlalchemy
from sqlalchemy.orm import sessionmaker

import schema
import config

create_plant_actions = ['create', 'create_plant']
actions = ['migrate', *create_plant_actions, 'list', 'create_mm', 'list_mm']
name_required = [*create_plant_actions, 'create_mm']

parser = argparse.ArgumentParser()
parser.add_argument("action", choices=actions, help="the action to be done")
parser.add_argument("--name", help="the name of the plant to be created")
args = parser.parse_args()

if args.action in name_required and args.name is None:
    parser.error(f'{args.action} action requires --name')

engine = sqlalchemy.create_engine('sqlite:///'+config.DB.path)

if args.action == 'migrate':
    schema.Base.metadata.create_all(engine)
    print('Done')

session = sessionmaker(bind=engine)()

if args.action in create_plant_actions:
    plant = schema.Plant(name=args.name)
    session.add(plant)
    session.commit()
    print(f'{args.name} created')

if args.action == 'create_mm':
    mmtype = schema.MMType(name=args.name)
    session.add(mmtype)
    session.commit()
    print(f'{args.name} created')

if args.action == 'list':
    for plant in session.query(schema.Plant).all():
        print(plant)

if args.action == 'list_mm':
    for mmtype in session.query(schema.MMType).all():
        print(mmtype)
