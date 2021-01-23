from keyboardcontroller import Controller,rgbToHIDBuf,modeToHIDBuf,LightingMode,KeyboardMatrix
from time import sleep
from random import randint,uniform
from ..audio import AudioController
from colors import hsv2rgb
import math
import asyncio

class AudioVisualizer:
    """ Audio visualizer class for keyboard.
        convert audio data to Keyboard Matrix
    """
    def __init__(self, threshold=1000, fade=0.8, delay=0.05, color_correction=(1,1,1)):
        """
        @param threshold - Threshold to clamp audio data when reached. Maximum audio level from input.
        @param fade - fade constant, higher the value, longer the fade effect will last. Between 0-1
        @param delay - how long to wait between each read from audio
        @param color_correction - Color correction for keyboard RGB values
        """

        self.kbcolors = KeyboardMatrix()
        self.keyboard = Controller()
        self.audio = AudioController()

        self.r=0
        self.g=0
        self.b=0

        self.threshold = threshold
        self.fade = fade
        self.delay = delay
        self.color_correction=color_correction

    async def visualizeOnce(self):
        """ Visualize current levels of audio on the keyboard, and render it
        """
        #audio data from stream (after fft)
        data = self.audio.readOnce()

        #for each column of keyboard
        for i in range(len(self.kbcolors.red[0])):
            for j in range(6):

                #fade out old values
                self.kbcolors.red[j][i]=math.floor(self.kbcolors.red[j][i]*self.fade)
                self.kbcolors.green[j][i]=math.floor(self.kbcolors.green[j][i]*self.fade)
                self.kbcolors.blue[j][i]=math.floor(self.kbcolors.blue[j][i]*self.fade)

        #sanitize data, in case of -inf and division by zeroes    
        for i in range(len(self.kbcolors.red[0])):
            d = data[i]
            if(d<0): d=0
            if(d>self.threshold):
                d = self.threshold
            
            #re-range the value between 0-6
            d = math.floor(d/self.threshold*6)

            #depending on the fft level, rows for columns
            for j in range(d):
                if self.kbcolors.red[j][i] <= self.r:
                    self.kbcolors.red[j][i] += int(self.r * (1-self.fade))
                    if self.kbcolors.red[j][i] > self.r: self.kbcolors.red[j][i]=self.r
                if self.kbcolors.green[j][i] <= self.g: 
                    self.kbcolors.green[j][i] += int(self.g * (1-self.fade))
                    if self.kbcolors.green[j][i] > self.g: self.kbcolors.green[j][i]=self.g
                if self.kbcolors.blue[j][i] <= self.b: 
                    self.kbcolors.blue[j][i] += int(self.b * (1-self.fade))
                    if self.kbcolors.blue[j][i] > self.g: self.kbcolors.blue[j][i]=self.g
            
        #render colors
        self.kbcolors.setKeyboardFlat(self.keyboard)

    async def visualize(self):
        """ Loop visualizeOnce infinitely
        """
        while True:
            await self.visualizeOnce()
            await asyncio.sleep(self.delay)

    async def change_color(self,r,g,b):
        """ Change color, use color corrections
        """
        self.r=int(r*self.color_correction[0])
        self.g=int(g*self.color_correction[1])
        self.b=int(b*self.color_correction[2])
        


