

from keyboardcontroller import Controller,rgbToHIDBuf,modeToHIDBuf,hsv2rgb,LightingMode,KeyboardMatrix
from time import sleep
from audio import AudioController

import pyaudio



audio = AudioController()
keyboard = Controller()

print(audio.readOnce())




r=0xff
g=0
b=0




while True:
    for data in heartbeat:
        j =hidDLL.HidD_SetFeature(int(device.hid_handle), create_string_3edc(data),len(data))
        #report[0].set_raw_data(i)
        sleep(0.1)
