import SendData
import time
from DartWZS import wzs, DartMode
from sense_hat import SenseHat
from SGP30 import my_sgp30

my_sgp30.initialize()

time.sleep(20)

sense = SenseHat()

wzs.initialize()

wzs.SwitchMode(DartMode.Manual)
wzs.ReadOnce()
wzs.SendReadCMD()
wzs.ReadOnce()

while 1:
    try:
        print (time.localtime(time.time()))

        # Get HCHO
        wzs.SendReadCMD()
        hcho = wzs.ReadOnce()
        if hcho < 0:
            print ("fail to get HCHO")
            continue
        print ('Get HCHO = %f'%hcho)

        # Get Temperature & Humidity
        temperature = sense.get_temperature()
        humidity = sense.get_humidity()
        pressure = sense.get_pressure()
        print ('Get temperature = {}, humidity = {}, pressure = {}'.format(temperature, humidity, pressure))

        # Get TVOC
        tvoc = my_sgp30.read_TVOC()
        print ('Get TVOC = %dppb'%tvoc)

        # Send data to server
        SendData.send_air_data(HCHO = hcho, Temperature = temperature, Humidity = humidity, TVOC = tvoc)
        print ('Data sent.')
    except Exception as ex:
        print (ex)
        continue
    finally:
        time.sleep(30*60)


wzs.deinitialize()
my_sgp30.deinitialize()
