import socket
import json

from csms import CSMS
from tinyserver import miniServer, miniRequestHandler

csms = CSMS()

def do_data():
    from db import DBConnection
    from schema import Point
    conn = DBConnection()
    return json.dumps([pt.to_dict(names=False) for pt in conn.session.query(Point).all()])

def do_meta():
    from db import DBConnection
    from schema import Plant, MMType
    conn = DBConnection()
    return json.dumps({
        'plants': [{'id':plant.id, 'name':plant.name} for plant in conn.session.query(Plant).all()],
        'types': [{'id':type_.id, 'name':type_.name} for type_ in conn.session.query(MMType).all()],
    })

class csmsRequestHandler(miniRequestHandler):
    _content_type = 'application/json'

    def message(self):
        if self.path == '/data':
            return do_data()
        if self.path == '/meta':
            return do_meta()
        return json.dumps({
            'relative': csms.relative
        })

class csmsServer(miniServer):
    address_family = socket.AF_INET6

csmsServer(request_handler=csmsRequestHandler, ip="::")

