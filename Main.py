import SendData
import time
from DartWZS import wzs, DartMode

wzs.initialize()


wzs.SwitchMode(DartMode.Manual)
wzs.ReadOnce()
wzs.SendReadCMD()
wzs.ReadOnce()

while 1:
    wzs.SendReadCMD()
    hcho = wzs.ReadOnce()
    print hcho
    if hcho < 0:
        print "fail to get HCHO"
    print 'Get HCHO = %f'%hcho
    SendData.send_hcho(hcho)
    time.sleep(60)


wzs.deinitialize()