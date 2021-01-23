"""@package docstring
A RGB keyboard interface for windows devices.
"""

from pywinusb import hid
from ctypes import *

from keyboard_matrix import KeyboardMatrix
from helpers import rgb_to_hid_buf

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
 
