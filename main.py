import json

from csms import CSMS
from miniserver import miniServer, miniRequestHandler

csms = CSMS()

class csmsRequestHandler(miniRequestHandler):
    def message(self):
        return json.dumps({
            'relative': csms.relative
        })

miniServer(request_handler=csmsRequestHandler)
