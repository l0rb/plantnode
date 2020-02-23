
from csms import CSMS
from db import DBConnection

csms = CSMS()
conn = DBConnection()

plant_id = 1
type_id = 1
conn.measure(csms.relative, 1, 1)
