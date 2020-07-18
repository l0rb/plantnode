import socket
import json
import urllib
import datetime

from tinyserver import miniServer, miniRequestHandler

def do_data(start):
    from db import DBConnection
    from schema import Point
    conn = DBConnection()
    query = conn.session.query(Point).filter(Point.time>datetime.datetime.fromtimestamp(start)).all()
    return json.dumps([pt.to_dict(names=False) for pt in query])

def do_meta():
    from db import DBConnection
    from schema import Plant, MMType
    conn = DBConnection()
    return json.dumps({
        'plants': [{'id':plant.id, 'name':plant.name} for plant in conn.session.query(Plant).all()],
        'types': [{'id':type_.id, 'name':type_.name} for type_ in conn.session.query(MMType).all()],
    })

def do_humid():
    from csms import CSMS
    csms = CSMS()
    return json.dumps([
        {'plant_id': 1, 'relative': csms.relative0},
        {'plant_id': 2, 'relative': csms.relative1}
    ])

def do_info(pp, rh):
    from db import DBConnection
    from schema import Point
    conn = DBConnection()
    return json.dumps({
        'status': 'ok',
        'path': pp.path,
        'query': urllib.parse.parse_qs(pp.query),
        'rline': rh.requestline,
    });


class csmsRequestHandler(miniRequestHandler):
    _content_type = 'application/json'

    def message(self):
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        query = urllib.parse.parse_qs(parsed_path.query)
        if path == '/data':
            start = 0
            if 'start' in query:
                start = int(query['start'])
            return do_data(start)
        if path == '/meta':
            return do_meta()
        if path == '/info':
            return do_info(parsed_path, self)
        return do_humid()

class csmsServer(miniServer):
    address_family = socket.AF_INET6

csmsServer(request_handler=csmsRequestHandler, ip="::")

