import SendData
import time
from DartWZS import wzs, DartMode

wzs.initialize()


wzs.SwitchMode(DartMode.Manual)
wzs.ReadOnce()
wzs.SendReadCMD()
wzs.ReadOnce()

while 1:
    try:
        print time.localtime(time.time())
        wzs.SendReadCMD()
        hcho = wzs.ReadOnce()
        if hcho < 0:
            print "fail to get HCHO"
        print 'Get HCHO = %f'%hcho
        SendData.send_hcho(hcho)
        print 'Sent.'
    except Exception as ex:
        print ex
    finally:
        time.sleep(600)


wzs.deinitialize()