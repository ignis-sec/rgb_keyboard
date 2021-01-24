import argparse
import signal

#from aud_keyboard import AudioVisualizer,LightingMode
from .keyboard_controller import KeyboardHIDController
from .keyboard_matrix import KeyboardMatrix,RGBRenderer
from .lighting_mode import LightingMode,ExtendedModes
from .helpers import mode_to_hid_buf,rgb_to_hid_buf
import allogate as logging
import asyncio

def parseInputColor(c):
    if not c:
        return None
    try:
        if(len(c)==6):
            id = 0
            r = int(c[0:2],16)
            g = int(c[2:4],16)
            b = int(c[6:8],16)
            logging.pprint(f"color set: {id}: {r},{g},{b}", 2)
            return (id,r,g,b)
        elif(len(c)==8):
            id = int(c[0])    
            r = int(c[2:4],16)
            g = int(c[4:6],16)
            b = int(c[6:8],16)
            logging.pprint(f"color set: {id}: {r},{g},{b}", 2)
            return (id,r,g,b)
        else:
            logging.pprint(f"Could not parse color: {c}")
            exit(1)
    except:
        return None

def runExtendedMode(renderer, mode, color):
    asyncio.run(getattr(RGBRenderer, mode)(renderer, color))

