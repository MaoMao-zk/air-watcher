import os, sys
import time
import board
import busio
import adafruit_sgp30

data_dir = "/usr/share/SGP30"
data_file = data_dir + "/data"

class _SGP30:
    def __init__(self):
        self._inited = False
        self._elapsed_sec = 0
        self._12h_baseline_seted = False
        self._times = 0 # n*10s
        self._baseline_eCO2 = 0
        self._baseline_TVOC = 0

    def initialize(self):
        if self._inited == True:
            return True
        i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)
        self._sgp30 = adafruit_sgp30.Adafruit_SGP30(i2c)
        print("SGP30 serial #", [hex(i) for i in self._sgp30.serial])
        self._sgp30.iaq_init()
        
        # TODO: read/save baselne in file
        os.listdir(data_dir)
        
        return True

    def readdata(self):
        if self._inited == False:
            return -1
        
        tvoc = self._sgp30.TVOC
        print("eCO2 = %d ppm \t TVOC = %d ppb" % (self._sgp30.eCO2, tvoc))
        
        self._elapsed_sec += 1
        if self._elapsed_sec > 10:
            self._elapsed_sec = 0
            print("**** Baseline values: eCO2 = 0x%x, TVOC = 0x%x"
                % (self._sgp30.baseline_eCO2, self._sgp30.baseline_TVOC))

        return tvoc

my_sgp30 = _SGP30()
my_sgp30.initialize()