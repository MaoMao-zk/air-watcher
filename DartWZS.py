from enum import Enum
import time
import serial

CMD_SwitchManual = b"\xFF\x01\x78\x41\x00\x00\x00\x00\x46"
CMD_SwitchAuto = b"\xFF\x01\x78\x40\x00\x00\x00\x00\x47"
CMD_Read = b"\xFF\x01\x86\x00\x00\x00\x00\x00\x79"

class DartMode(Enum):
    Unset = 0
    Auto = 1
    Manual = 2

class _DartWZS:
    def __init__(self):
        self._inited = False
        self._mode = DartMode.Unset

    def initialize(self):
        if self._inited == True:
            return True
        self._serial = serial.Serial ("/dev/ttyS0", 9600, timeout=2)
        self._inited = self._serial.isOpen()
        return self._inited

    def deinitialize(self):
        if False == self._inited:
            return
        self._inited = False
        self._mode = DartMode.Unset
        self._serial.close()

    def SwitchMode(self, mode):
        if self._mode == mode:
            return True;
        if self._inited == False:
            return False;
        if mode == DartMode.Auto:
            print ("Set to auto")
            print ("CMD_SwitchAuto %d"%self._serial.write(CMD_SwitchAuto))
            self._mode = mode
            return True
        elif mode == DartMode.Manual:
            print ("Set to manual")
            print ("CMD_SwitchManual %d"%self._serial.write(CMD_SwitchManual))
            self._mode = mode
            return True
        else:
            return False

    def SendReadCMD(self):
        if self._mode != DartMode.Manual:
            return False;
        print ("CMD_Read %d"%self._serial.write(CMD_Read))

    def ReadOnce(self):
        hcho = -0.1;
        try:
            data = self._serial.read(9)
        except:
            print ("Read data timeout.")
            return hcho

        if len(data) < 9:
            print ("only read %d data"%len(data))
            return hcho
        """
        for i in data:
            print('%#x'%ord(i))
        print '---------------------------------'
        """

        if 0x78 == data[1]:
            if 0x40 == data[2]:
                self._mode = DartMode.Auto
            else:
                self._mode = DartMode.Manual
            print ("Current mode is " + str(self._mode))
        elif 0x17 == data[1]:
            hcho = (data[4]*255+data[5]) * 1.2258 / 1000
        elif 0x86 == data[1]:
            hcho = float(data[2]*255 + data[3]) / 1000
        return hcho


wzs = _DartWZS()