import board

from dht11 import DHT11
from csms import CSMS
from db import DBConnection

efeutopf = 1
monstera = 2

csms = CSMS()
conn = DBConnection()

conn.measure(csms.relative, efeutopf, 1)
conn.measure(csms.relative1, monstera, 1)

dht = DHT11(board.D10)
air_temp, air_humid = dht.average()

conn.measure(air_temp, efeutopf, 2)
conn.measure(air_humid, efeutopf, 3)

