import time
import logging

import board
import adafruit_dht
 
class DHT11(adafruit_dht.DHT11):
    def __init__(self, *args, **kwargs):
        self.device = super().__init__(*args, **kwargs)

    def measure(self, limit=10):
        delay = 2.05 # needs to be at least 2. check adafruit implementation for reason
        attempt = 0
        while limit==0 or attempt<limit:
            attempt += 1
            try:
                super().measure()
                break
            except RuntimeError as error:
                # Errors happen fairly often, DHT's are hard to read, just keep going
                logging.info(error.args[0])
                time.sleep(delay)

    def both(self):
        self.measure()
        return (self._temperature, self._humidity)

    def average(self, n=5):
        delay = 2.05 # need to wait at least 2s to make an actual new measurement
        temp = 0
        hum = 0
        for i in range(0, n):
            self.measure()
            temp += self._temperature
            hum += self._humidity
            time.sleep(delay)
        return temp/n, hum/n

