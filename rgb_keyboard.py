

import argparse
#from aud_keyboard import AudioVisualizer,LightingMode
from keyboard_controller import KeyboardHIDController
from lighting_mode import LightingMode
from helpers import mode_to_hid_buf,rgb_to_hid_buf


if __name__=="__main__":

    parser = argparse.ArgumentParser(description='RGB Keyboard CLI')

    parser.add_argument("-v","--verbose", action="count", help="Set verbosity level")
    parser.add_argument("-m","--mode", help="Lighting Mode")
    parser.add_argument("-s","--speed", help="Effect speed")
    parser.add_argument("-r","--rotation", help="Effect rotation")
    parser.add_argument("-c","--color", action="store_true",help="give a file instead of cli text")

    args = parser.parse_args() 

    keyboard =KeyboardHIDController()
    keyboard.reset_colors()
    keyboard.send(mode_to_hid_buf(LightingMode.WAVE, speed=1))