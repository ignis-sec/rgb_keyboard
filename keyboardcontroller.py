"""@package docstring
A RGB keyboard interface for windows devices.
"""
from pywinusb import hid
from time import sleep
from ctypes import *
import win32file
import colorsys



class KeyboardMatrix():
    """A keyboard matrix class holding RGB values for all keys
    """
    def __init__(self):
        self.red = [
            [0]*21,
            [0]*21,
            [0]*21,
            [0]*21,
            [0]*21,
            [0]*21
        ]
        self.green = [
            [0]*21,
            [0]*21,
            [0]*21,
            [0]*21,
            [0]*21,
            [0]*21
        ]*6
        self.blue = [
            [0]*21,
            [0]*21,
            [0]*21,
            [0]*21,
            [0]*21,
            [0]*21
        ]*6



    def make_keyboard_buffer(self):
        """Convert self.red, self.green and self.blue to keyboard buffer needed for interface

        key values are written to output report, while updates are done via features report.
        
        Following will be written over USB for each row (bottom-up):
        b"\\x00\\x00" + bytes(self.blue[i]) + bytes(self.green[i]) + bytes(self.red[i])
        """

        ret = []

        # set 6x21 array for return buffer
        buf = b""
        for i in range(6):
            buf = b"\x00\x00" + bytes(self.blue[i]) + bytes(self.green[i]) + bytes(self.red[i])
            ret.append(buf)
    
        return ret

    
    def set_keyboard_flat(self, keyboard, r=None,g=None,b=None):
        """Set keyboard to flat color.
        If either of r/g/b values are given, all the keys will be set to the same color. If not, stored colors will be used.

        For each row of keyboard, send feature request:
            b"\\x00\\x16\\x00" + bytes([i])  + b"\\x00\\x00\\x00\\x00\\x00"

        And send the corresponding color data through output report.

        Finalize with a render request:
        b"\\x00\\x16\\x12\\x00\\x00\\x08\\x01\\x00\\x00\\x00"
        """

        #set r/g/b values if specified
        if(r):
            for i in range(6):
                for j in range(21):
                    self.red[i][j] = r
        
        if(g):
            for i in range(6):
                for j in range(21):
                    self.green[i][j] = g

        if(b):
            for i in range(6):
                for j in range(21):
                    self.blue[i][j] = b

        #send set color request
        keyboard.send(mode_to_hid_buf( mode=LightingMode.FLAT_COLOR, speed=48, brightness=48))

        #for each of the keyboard rows, send notification via feature request, and send the corresponding color data
        d = self.make_keyboard_buffer()

        for i in range(6):
            keyboard.send(b"\x00\x16\x00" + bytes([i])  + b"\x00\x00\x00\x00\x00")
            keyboard.output.send(d[i])
        
        #render colors
        keyboard.send(b"\x00\x16\x12\x00\x00\x08\x01\x00\x00\x00")
   


class LightingMode():
    """ Enum class for different lighting methods and their corresponding values
    """
    BREATHING       = b"\x02" 
    WAVE            = b"\x03"
    TOUCH           = b"\x04" 
    RAINBOW         = b"\x05"
    RIPPLE          = b"\x06"
    SNAKE           = b"\x09"
    RAINDROP        = b"\x0a"
    AURORA          = b"\x0e"
    FIRECRACKER     = b"\x11"
    FLAT_COLOR      = b"\x33"




def rgb_to_hid_buf(r,g,b, id=1):
    """ Convert RGB colors to HID message buffer
    """
    if(id>8):
        return False
    return b"\x00\x14\x00" + bytes([id,r,g,b]) + b"\x00\x00"

def mode_to_hid_buf(mode=b"\x00\x00", speed=0, brightness=32, a=0,rotation=0,c=0):
    """ Convert lighting mode to HID message buffer
    """
    return b"\x00\x08\x02" + mode + bytes([speed,brightness,a,rotation,c])


class KeyboardHIDController:
    """ Class for interfacing with HID keyboard data

    By default;
    vendor_id = 0x048d, product_id = 0xce00
    """
    def __init__(self, vendor_id = 0x048d, product_id = 0xce00, index=1):
        
        #find hid device
        filter = hid.HidDeviceFilter(vendor_id = vendor_id, product_id = product_id)
        self.hid_devices = filter.get_devices()
        self.device = self.hid_devices[index]
        
        #hook hid.dll from system32
        self.hid_dll = WinDLL("hid")

        #target_usage = hid.get_full_usage_id(0xff03, 0x01)
        #print(hex(target_usage))

        self.device.open()

        #open all reports
        self.report = self.device.find_any_reports()
        
        self.output = self.report[1][0]
        

    def send(self,data):
        """ Send feature report to HID device
        """
        
        return self.hid_dll.HidD_SetFeature(int(self.device.hid_handle), create_string_buffer(data),len(data))
        

    def reset_colors(self):
        """ Reset colors to default
        """
        self.send(rgb_to_hid_buf(0xff, 0x00, 0x00, 1))
        self.send(rgb_to_hid_buf(0xff, 0x1e, 0x00, 2))
        self.send(rgb_to_hid_buf(0xff, 0x64, 0x00, 3))
        self.send(rgb_to_hid_buf(0x00, 0x64, 0x00, 4))
        self.send(rgb_to_hid_buf(0x00, 0x00, 0x50, 5))
        self.send(rgb_to_hid_buf(0x00, 0x64, 0x00, 6))
        self.send(rgb_to_hid_buf(0xff, 0x00, 0x50, 7))


    async def rainbow_fade(self):
        """ Rainbow Fade effect
        """

        kbcolors = KeyboardMatrix()
        r=0xff
        g=0
        b=0
        while True:
            for g in range(0,0x1e):
                kbcolors.set_keyboard_flat(self, r=r, g=g, b=b)
            for g in range(0x1e, 0x50):
                kbcolors.set_keyboard_flat(self, r=r, g=g, b=b)
            for r in range(0xff, 0x00, -1):
                kbcolors.set_keyboard_flat(self, r=r, g=g, b=b)
            for b in range(0x00, 0x50):
                kbcolors.set_keyboard_flat(self, r=r, g=g-b, b=b)
            g=0
            for r in range(0x00, 0xff):
                kbcolors.set_keyboard_flat(self, r=r, g=g, b=b)
            for b in range(0x50, 0x00, -1):
                kbcolors.set_keyboard_flat(self, r=r, g=g, b=b)
 