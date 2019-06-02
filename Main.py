import SendData
import time
from DartWZS import wzs, DartMode
from sense_hat import SenseHat

time.sleep(10)

sense = SenseHat()

wzs.initialize()


wzs.SwitchMode(DartMode.Manual)
wzs.ReadOnce()
wzs.SendReadCMD()
wzs.ReadOnce()

while 1:
    try:
        print time.localtime(time.time())

        # Get HCHO
        wzs.SendReadCMD()
        hcho = wzs.ReadOnce()
        if hcho < 0:
            print "fail to get HCHO"
            continue
        print 'Get HCHO = %f'%hcho

        # Get Temperature & Humidity
        temperature = sense.get_temperature()
        humidity = sense.get_humidity()
        pressure = sense.get_pressure()
        print 'Get temperature = {}, humidity = {}, pressure = {}'.format(temperature, humidity, pressure)

        # Send data to server
        SendData.send_air_data(HCHO = hcho, Temperature = temperature, Humidity = humidity)
        print 'Data sent.'
    except Exception as ex:
        print ex
        continue
    finally:
        time.sleep(30*60)


wzs.deinitialize()
