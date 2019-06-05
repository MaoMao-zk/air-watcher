import os, sys
import threading
import time
import board
import busio
import adafruit_sgp30

data_dir = "/usr/share/SGP30"
data_file = data_dir + "/data"

class _SGP30(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self._inited = False
        self._elapsed_sec = 0
        self._12h_baseline_seted = False
        self._times = 0 # n*10s

    def initialize(self):
        if self._inited == True:
            return True
        
        # 0. Init device
        i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)
        self._sgp30 = adafruit_sgp30.Adafruit_SGP30(i2c)
        print("SGP30 serial #", [hex(i) for i in self._sgp30.serial])
        self._sgp30.iaq_init()
        
        # 1. Check data dir
        try:
            os.listdir(data_dir)
        except:
            # dir might not exsit
            os.mkdir(data_dir)
        
        # 2. Open data file and read data
        self._data_file = open(data_file, mode="r+")
        line = self._data_file.readline()
        print("Readline -> " + line)
        if line != "":
            datas = line.split(',')
            self._times = int(datas[0])
            if self._times < 12*60*60:
                self._times = 0
            baseline_eCO2 = int(datas[1])
            baseline_TVOC = int(datas[2])
            print("**** Read Baseline from file: eCO2 = 0x%x, TVOC = 0x%x"
                % (baseline_eCO2, baseline_TVOC))
            
            if self._times > 12*60*60:
                self._sgp30.set_iaq_baseline(baseline_eCO2, baseline_TVOC)
        
        # 3. Create thread get tvoc data
        self._thread_runing = True
        self.start()
        self._inited = True
        return True

    def deinitialize(self):
        if False == self._inited:
            return
        self._inited = False
        
        assert(self.is_alive())
        self._thread_runing = False
        self.join(timeout=2)

        self._data_file.close()
    
    def run(self):
        while self._thread_runing:
            print("eCO2 = %d ppm \t TVOC = %d ppb" % (self._sgp30.eCO2, self._sgp30.TVOC))
            
            self._elapsed_sec += 1
            if self._elapsed_sec > 10:
                self._elapsed_sec = 0
                print("**** Baseline values: eCO2 = 0x%x, TVOC = 0x%x"
                    % (self._sgp30.baseline_eCO2, self._sgp30.baseline_TVOC))
                if self._times <= 12*60*60:
                    self._times += 10
                self._data_file.seek(0)
                self._data_file.write(str(self._times) + ',' + str(self._sgp30.baseline_eCO2) + ',' + str(self._sgp30.baseline_TVOC) + '\n')
                self._data_file.flush()
            
            time.sleep(1)

    def read_TVOC(self):
        if self._thread_runing == False:
            return -1
        return self._sgp30.TVOC

my_sgp30 = _SGP30()

""" Sample
my_sgp30.initialize()
print("initialized")

time.sleep(50)

my_sgp30.deinitialize()
print("deinitialized")
"""