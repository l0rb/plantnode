import json

from csms import CSMS
from tinyserver import miniServer, miniRequestHandler

csms = CSMS()

def do_data():
    from db import DBConnection
    from schema import Point
    conn = DBConnection()
    return json.dumps({conn.session.query(Point).all()})

class csmsRequestHandler(miniRequestHandler):
    def message(self):
        if self.path == '/data':
            return do_data()
        return json.dumps({
            'relative': csms.relative
        })

miniServer(request_handler=csmsRequestHandler)
