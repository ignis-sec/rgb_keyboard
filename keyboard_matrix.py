
from .lighting_mode import LightingMode
from .helpers import mode_to_hid_buf
from .aud_keyboard import AudioVisualizer
from .audio_loopback.audio_visualizer import AudioVisualizer2D,ColorMatrix
import allogate as logging

class KeyboardMatrix(ColorMatrix):

    def make_keyboard_buffer(self):
        """Convert self.red, self.green and self.blue to keyboard buffer needed for interface

        key values are written to output report, while updates are done via features report.
        
        Following will be written over USB for each row (bottom-up):
        b"\\x00\\x00" + bytes(self.blue[i]) + bytes(self.green[i]) + bytes(self.red[i])
        """

        ret = []
        logging.pprint(f"Creating Keyboard RGB Matrix", 5)
        # set 6x21 array for return buffer
        buf = b""
        for i in range(6):
            buf = b"\x00\x00" + bytes(self.blue[i]) + bytes(self.green[i]) + bytes(self.red[i])
            ret.append(buf)
    
        return ret

    
    def render(self, r=None,g=None,b=None):
        """Set keyboard to flat color.
        If either of r/g/b values are given, all the keys will be set to the same color. If not, stored colors will be used.

        For each row of keyboard, send feature request:
            b"\\x00\\x16\\x00" + bytes([i])  + b"\\x00\\x00\\x00\\x00\\x00"

        And send the corresponding color data through output report.

        Finalize with a render request:
        b"\\x00\\x16\\x12\\x00\\x00\\x08\\x01\\x00\\x00\\x00"
        """

        logging.pprint(f"Setting flat color", 4)
        #set r/g/b values if specified
        if(r):
            logging.pprint(f"Red color given, will fill the keyboard", 5)
            for i in range(6):
                for j in range(21):
                    self.red[i][j] = r
        
        if(g):
            logging.pprint(f"Green color given, will fill the keyboard", 5)
            for i in range(6):
                for j in range(21):
                    self.green[i][j] = g

        if(b):
            logging.pprint(f"Blue color given, will fill the keyboard", 5)
            for i in range(6):
                for j in range(21):
                    self.blue[i][j] = b

        #send set color request
        self.device.send(mode_to_hid_buf( mode=LightingMode.FLAT_COLOR, speed=48, brightness=48))

        #for each of the keyboard rows, send notification via feature request, and send the corresponding color data
        d = self.make_keyboard_buffer()

        for i in range(6):
            self.device.send(b"\x00\x16\x00" + bytes([i])  + b"\x00\x00\x00\x00\x00")
            logging.pprint(f"col {i}: {d[i]}", 5)
            self.device.output.send(d[i])
        
        #render colors
        self.device.send(b"\x00\x16\x12\x00\x00\x08\x01\x00\x00\x00")
   


class RGBRenderer(KeyboardMatrix):
    """ Class derived from Keyboard Matrix
        Also capable of rendering complex colors and animations
    """ 
    def __init__(self, keyboard):
        super().__init__(keyboard)
    
    async def rainbow_fade(self, c):
        """ Rainbow Fade effect
        """
        logging.pprint(f"Starting rainbow fade effect.", 2)
        
        r=0xff
        g=0
        b=0
        while True:
            for g in range(0,0x1e):
                self.render(r=r, g=g, b=b)
            for g in range(0x1e, 0x50):
                self.render(r=r, g=g, b=b)
            for r in range(0xff, 0x00, -1):
                self.render(r=r, g=g, b=b)
            for b in range(0x00, 0x50):
                self.render(r=r, g=g-b, b=b)
            g=0
            for r in range(0x00, 0xff):
                self.render(r=r, g=g, b=b)
            for b in range(0x50, 0x00, -1):
                self.render(r=r, g=g, b=b)

    async def audio_visualizer(self, c):
        visualizer = AudioVisualizer2D(self)
        await visualizer.change_color(255,255,0)
        await visualizer.visualize()