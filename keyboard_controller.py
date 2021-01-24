"""@package docstring
A RGB keyboard interface for windows devices.
"""

from pywinusb import hid
from ctypes import *

from helpers import rgb_to_hid_buf
import allogate as logging

class KeyboardHIDController:
    """ Class for interfacing with HID keyboard data

    By default;
    vendor_id = 0x048d, product_id = 0xce00
    """
    def __init__(self, vendor_id = 0x048d, product_id = 0xce00, index=1):
        logging.pprint(f"vendor_id:{hex(vendor_id)}, product_id:{hex(product_id)}", 3)
        #find hid device
        filter = hid.HidDeviceFilter(vendor_id = vendor_id, product_id = product_id)
        self.hid_devices = filter.get_devices()

        logging.pprint("HID devices (filtered): ", 3)
        for device in self.hid_devices:
            logging.pprint(f"\t{device}", 3)
        self.device = self.hid_devices[index]
        
        #hook hid.dll from system32
        self.hid_dll = WinDLL("hid")

        #target_usage = hid.get_full_usage_id(0xff03, 0x01)
        #print(hex(target_usage))

        self.device.open()
        logging.pprint("Opened HID device with handle: {self.device.hid_handle}", 3)

        #open all reports
        self.report = self.device.find_any_reports()
        self.output = self.report[1][0] 
        logging.pprint(f"Input   reports:{self.report[0]}", 3)
        logging.pprint(f"Output  reports:{self.report[1]}", 3)
        logging.pprint(f"Feature reports:{self.report[2]}", 3)
        logging.pprint(f"{self.report[0][0]}", 3)
        logging.pprint(f"{self.report[1][0]}", 3)
        logging.pprint(f"{self.report[2][0]}", 3)


    def send(self,data):
        """ Send feature report to HID device
        """
        logging.pprint(f"Sending: {data}", 6)
        return self.hid_dll.HidD_SetFeature(int(self.device.hid_handle), create_string_buffer(data),len(data))
        

    def reset_colors(self):
        """ Reset colors to default
        """
        logging.pprint(f"Resetting colors", 2)
        self.send(rgb_to_hid_buf(0xff, 0x00, 0x00, 1))
        self.send(rgb_to_hid_buf(0xff, 0x1e, 0x00, 2))
        self.send(rgb_to_hid_buf(0xff, 0x64, 0x00, 3))
        self.send(rgb_to_hid_buf(0x00, 0x64, 0x00, 4))
        self.send(rgb_to_hid_buf(0x00, 0x00, 0x50, 5))
        self.send(rgb_to_hid_buf(0x00, 0x64, 0x00, 6))
        self.send(rgb_to_hid_buf(0xff, 0x00, 0x50, 7))
 
