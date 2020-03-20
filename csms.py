import time
from time import sleep

import busio
import board

import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn


class CSMS():
    def __init__(self, v_max=2.79, v_min=1.42):
        """
            v_max and v_min are not super accurate.

            The highest v_max I have seen so far was ~2.7859 physically
            suspending the cable in air on a dry winter day, right
            after bathing it for the v_min

            v_min has been obtained by submerging the sensor in a
            glass of water. had to "soak" for about 3 minutes
            to reach the lowest seen-so-far of ~1.4231

            These may also depend on the source current, which
            I'm using the zeros 5V for.
        """
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.ads = ADS.ADS1115(self.i2c)
        self.channels = list():
        for ads_px in [ADS.P0, ADS.P1, ADS.P2, ADS.P3]:
            self.channels.append(AnalogIn(self.ads, ads_px))
        self.v_max = v_max
        self.v_min = v_min
        self.v_range = v_max - v_min

    @property
    def voltage(self):
        return self.channel[0].voltage

    @property
    def value(self):
        return self.channel[0].value

    @property
    def relative(self):
        return 1 - (self.voltage - self.v_min ) / self.v_range


if __name__ == '__main__':
    csms = CSMS()
    print("Voltage", csms.voltage)
    print("Relative", csms.relative)
