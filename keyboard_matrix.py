
from lighting_mode import LightingMode
from helpers import mode_to_hid_buf

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
   
