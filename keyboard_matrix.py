
from lighting_mode import LightingMode
from helpers import mode_to_hid_buf
import logging

class KeyboardMatrix():
    """A keyboard matrix class holding RGB values for all keys
    """
    def __init__(self, keyboard):
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
        self.keyboard=keyboard

    def make_keyboard_buffer(self):
        """Convert self.red, self.green and self.blue to keyboard buffer needed for interface

        key values are written to output report, while updates are done via features report.
        
        Following will be written over USB for each row (bottom-up):
        b"\\x00\\x00" + bytes(self.blue[i]) + bytes(self.green[i]) + bytes(self.red[i])
        """

        ret = []
        logging.pprint(f"Creating Keyboard RGB Matrix", 4)
        # set 6x21 array for return buffer
        buf = b""
        for i in range(6):
            buf = b"\x00\x00" + bytes(self.blue[i]) + bytes(self.green[i]) + bytes(self.red[i])
            logging.pprint(f"col {i}: {buf}", 4)
            ret.append(buf)
    
        return ret

    
    def set_keyboard_flat(self, r=None,g=None,b=None):
        """Set keyboard to flat color.
        If either of r/g/b values are given, all the keys will be set to the same color. If not, stored colors will be used.

        For each row of keyboard, send feature request:
            b"\\x00\\x16\\x00" + bytes([i])  + b"\\x00\\x00\\x00\\x00\\x00"

        And send the corresponding color data through output report.

        Finalize with a render request:
        b"\\x00\\x16\\x12\\x00\\x00\\x08\\x01\\x00\\x00\\x00"
        """

        logging.pprint(f"Setting flat color", 2)
        #set r/g/b values if specified
        if(r):
            logging.pprint(f"Red color given, will fill the keyboard", 4)
            for i in range(6):
                for j in range(21):
                    self.red[i][j] = r
        
        if(g):
            logging.pprint(f"Green color given, will fill the keyboard", 4)
            for i in range(6):
                for j in range(21):
                    self.green[i][j] = g

        if(b):
            logging.pprint(f"Blue color given, will fill the keyboard", 4)
            for i in range(6):
                for j in range(21):
                    self.blue[i][j] = b

        #send set color request
        self.keyboard.send(mode_to_hid_buf( mode=LightingMode.FLAT_COLOR, speed=48, brightness=48))

        #for each of the keyboard rows, send notification via feature request, and send the corresponding color data
        d = self.make_keyboard_buffer()

        for i in range(6):
            self.keyboard.send(b"\x00\x16\x00" + bytes([i])  + b"\x00\x00\x00\x00\x00")
            self.keyboard.output.send(d[i])
        
        #render colors
        self.keyboard.send(b"\x00\x16\x12\x00\x00\x08\x01\x00\x00\x00")
   


class RGBRenderer(KeyboardMatrix):
    """ Class derived from Keyboard Matrix
        Also capable of rendering complex colors and animations
    """ 
    def __init__(self, keyboard):
        super().__init__(keyboard)
    
    def rainbow_fade(self):
        """ Rainbow Fade effect
        """
        logging.pprint(f"Starting rainbow fade effect.", 2)
        
        r=0xff
        g=0
        b=0
        while True:
            for g in range(0,0x1e):
                self.set_keyboard_flat(r=r, g=g, b=b)
            for g in range(0x1e, 0x50):
                self.set_keyboard_flat(r=r, g=g, b=b)
            for r in range(0xff, 0x00, -1):
                self.set_keyboard_flat(r=r, g=g, b=b)
            for b in range(0x00, 0x50):
                self.set_keyboard_flat(r=r, g=g-b, b=b)
            g=0
            for r in range(0x00, 0xff):
                self.set_keyboard_flat(r=r, g=g, b=b)
            for b in range(0x50, 0x00, -1):
                self.set_keyboard_flat(r=r, g=g, b=b)