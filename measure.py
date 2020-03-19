import board

from dht11 import DHT11
from csms import CSMS
from db import DBConnection

plant_id = 1

csms = CSMS()
conn = DBConnection()

conn.measure(csms.relative, plant_id, 1)

dht = DHT11(board.D10)
air_temp, air_humid = dht.average()

conn.measure(air_temp, plant_id, 2)
conn.measure(air_humid, plant_id, 3)

