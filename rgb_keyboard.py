

import argparse
import signal
#from aud_keyboard import AudioVisualizer,LightingMode
from keyboard_controller import KeyboardHIDController
from keyboard_matrix import KeyboardMatrix,RGBRenderer
from lighting_mode import LightingMode,ExtendedModes
from helpers import mode_to_hid_buf,rgb_to_hid_buf
import allogate as logging
import asyncio

def parseInputColor(c):
    if not c:
        return None
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

def runExtendedMode(renderer, mode, color):
    asyncio.run(getattr(RGBRenderer, mode)(renderer, color))

def signal_handler(sig, frame):
    keyboard.send(mode_to_hid_buf(mode=LightingMode.FLAT_COLOR, speed=speed, brightness=brightness, rotation=rotation))

if __name__=="__main__":
    parser = argparse.ArgumentParser(description='RGB Keyboard CLI')
    parser.add_argument("-v","--verbose", action="count", help="Set verbosity level")
    parser.add_argument("-m","--mode", help="Lighting Mode")
    parser.add_argument("-s","--speed", help="Effect speed")
    parser.add_argument("-r","--rotation", help="Effect rotation")
    parser.add_argument("-b","--brightness", help="Effect brightness")
    parser.add_argument("-c","--color", nargs='*', help="RGB color, id#rrggbb, hex. Id is between 1-7")
    args = parser.parse_args() 

    if args.verbose:
        logging.VERBOSITY=int(args.verbose)

    keyboard =KeyboardHIDController()
    keyboard.reset_colors()

    if(args.color):
        for c in args.color:
            id,r,g,b = parseInputColor(c)
            keyboard.send(rgb_to_hid_buf(r,g,b,id=id))

    brightness=32
    if(args.brightness):
        brightness=int(args.brightness)
        logging.pprint(f"Brightness: {brightness}",1)

    speed = 0
    if(args.speed):
        speed=int(args.speed)
        logging.pprint(f"speed: {speed}",1)

    
    rotation=0
    if(args.rotation):
        rotation=int(args.rotation)
        logging.pprint(f"Rotation: {rotation}",1)


    mode = LightingMode.WAVE
    extended_mode=None
    if(args.mode):
        try:
            mode = getattr(LightingMode, args.mode)
            logging.pprint(f"Lighting mode: LightingMode.{args.mode}",1)
            logging.pprint(f"LightingMode.{args.mode}: {mode}",2)
        except:
            try:
                logging.pprint(f"Failed to find mode, looking for extended modes.",2)
                extended_mode = getattr(ExtendedModes, args.mode)
                logging.pprint(f"Lighting mode: ExtendedModes.{args.mode}",1)
                logging.pprint(f"ExtendedModes.{args.mode}: {mode}",2)
            except:
                logging.pprint("Invalid mode name")
                exit(1)

    
    if(extended_mode):
        renderer = RGBRenderer(keyboard)
        if(args.color):
            c = parseInputColor(args.color)
        else:
            c = None
        if not c:
            c = (0,0xff,0x00,0x00)
        runExtendedMode(renderer, extended_mode, c)
        

    elif(mode==LightingMode.FLAT_COLOR):
        logging.pprint(f"Lighting mode set to LightingMode.FLAT_COLOR",1)
        kbcolors = KeyboardMatrix(keyboard)
        if(args.color):
            id,r,g,b = parseInputColor(args.color)
            kbcolors.set_keyboard_flat(r,g,b)
        else:
            logging.pprint("Need color for flat colors.")
            exit(1)
    else:
        logging.pprint(f"Rendering new colors",1)
        keyboard.send(mode_to_hid_buf(mode=mode, speed=speed, brightness=brightness, rotation=rotation))