
import math
import asyncio
from .audio_loopback.audio_loopback import AudioController


class AudioVisualizer:
    """ Audio visualizer class for keyboard.
        convert audio data to color_matrix
    """
    def __init__(self, color_matrix, ceiling=1220, fade=0.8, delay=0.05, color_correction=(1,1,1), ambient_glow=15, dampen=1000, dampen_bias=0.92, ceiling_bias=0.98):
        """
        @param ceiling - Threshold to clamp audio data when reached. Maximum audio level from input.
        @param fade - fade constant, higher the value, longer the fade effect will last. Between 0-1
        @param delay - how long to wait between each read from audio
        @param color_correction - Color correction for keyboard RGB values
        """

        self.color_matrix = color_matrix
        self.audio = AudioController()

        self.r=0
        self.g=0
        self.b=0

        self.ceiling = ceiling
        self.fade = fade
        self.delay = delay
        self.color_correction=color_correction

        self.dampen = dampen
        self.ambient_glow = ambient_glow
        self.dampen_bias = dampen_bias
        self.ceiling_bias = ceiling_bias

    def visualizeOnce(self):
        """ Visualize current levels of audio on the keyboard, and render it
        """
        #audio data from stream (after fft)
        data = self.audio.readOnce(25,20)

        #for each column of keyboard
        for i in range(len(self.color_matrix.red[0])):
            for j in range(6):

                #fade out old values
                self.color_matrix.red[j][i]=math.floor(self.color_matrix.red[j][i]*self.fade)
                self.color_matrix.green[j][i]=math.floor(self.color_matrix.green[j][i]*self.fade)
                self.color_matrix.blue[j][i]=math.floor(self.color_matrix.blue[j][i]*self.fade)

        #sanitize data, in case of -inf and division by zeroes

        current_dampening = self.dampen
        current_ceiling = self.ceiling    
        for i in range(len(self.color_matrix.red[0])):
            d = data[i]
            d = d - current_dampening
            if(d<self.ambient_glow): d=self.ambient_glow
            if(d>current_ceiling):
                d = current_ceiling
            
            #re-range the value between 0-6
            d = math.floor(d/(current_ceiling-current_dampening)*6)
            if(d>6): d=6

            current_dampening = current_dampening*self.dampen_bias
            current_ceiling = current_ceiling * self.ceiling_bias
            #depending on the fft level, rows for columns
            for j in range(d):
                if self.color_matrix.red[j][i] <= self.r:
                    self.color_matrix.red[j][i] += int(self.r * (1-self.fade))
                    if self.color_matrix.red[j][i] > self.r: self.color_matrix.red[j][i]=self.r
                if self.color_matrix.green[j][i] <= self.g: 
                    self.color_matrix.green[j][i] += int(self.g * (1-self.fade))
                    if self.color_matrix.green[j][i] > self.g: self.color_matrix.green[j][i]=self.g
                if self.color_matrix.blue[j][i] <= self.b: 
                    self.color_matrix.blue[j][i] += int(self.b * (1-self.fade))
                    if self.color_matrix.blue[j][i] > self.g: self.color_matrix.blue[j][i]=self.g
            
        #render colors
        self.color_matrix.render()

    async def visualize(self):
        """ Loop visualizeOnce infinitely
        """
        while True:
            self.visualizeOnce()
            await asyncio.sleep(self.delay)

    async def change_color(self,r,g,b):
        """ Change color, use color corrections
        """
        self.r=int(r*self.color_correction[0])
        self.g=int(g*self.color_correction[1])
        self.b=int(b*self.color_correction[2])
        


