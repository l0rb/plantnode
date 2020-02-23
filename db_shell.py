import argparse

from db import DBConnection
import schema

create_plant_actions = ['create', 'create_plant']
actions = ['migrate', *create_plant_actions, 'list', 'create_mm', 'list_mm']
name_required = [*create_plant_actions, 'create_mm']

parser = argparse.ArgumentParser()
parser.add_argument("action", choices=actions, help="the action to be done. actions that create new objects require --name")
parser.add_argument("--name", help="the name of the plant or measurement-type to be created")
args = parser.parse_args()

if args.action in name_required and args.name is None:
    parser.error(f'{args.action} action requires --name')

conn = DBConnection()

if args.action == 'migrate':
    conn.migrate()
    print('Done')

if args.action in create_plant_actions:
    conn.make_plant(args.name)
    print(f'{args.name} created')

if args.action == 'create_mm':
    conn.make_mm_type(args.name)
    print(f'{args.name} created')

if args.action == 'list':
    for plant in conn.session.query(schema.Plant).all():
        print(plant)

if args.action == 'list_mm':
    for mmtype in conn.session.query(schema.MMType).all():
        print(mmtype)
