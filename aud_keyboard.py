from keyboardcontroller import Controller,rgbToHIDBuf,modeToHIDBuf,LightingMode,KeyboardMatrix
from time import sleep
from random import randint,uniform
from audio import AudioController
from colors import hsv2rgb
import math
import asyncio






class AudioVisualizer:
    def __init__(self):
        self.kbcolors = KeyboardMatrix()
        self.kbcolors = KeyboardMatrix()
        self.keyboard = Controller()
        self.audio = AudioController()

        self.r=0
        self.g=0
        self.b=0

        self.threshold=1000
        self.fade = 0.8
        self.delay = 0.05

    async def visualize(self):
        while True:
            for i in range(len(self.kbcolors.red[0])):
                for j in range(6):
                    self.kbcolors.red[j][i]=math.floor(self.kbcolors.red[j][i]*self.fade)
                    self.kbcolors.green[j][i]=math.floor(self.kbcolors.green[j][i]*self.fade)
                    self.kbcolors.blue[j][i]=math.floor(self.kbcolors.blue[j][i]*self.fade)
            data = self.audio.readOnce()
            for i in range(len(self.kbcolors.red[0])):
                #print(data)
                #print(data[i])
                d = data[i]
                if(d<0): d=0
                if(d>self.threshold):
                    d = self.threshold
                
                

                d = math.floor(d/self.threshold*6)
                #print(d, end=', ')
                for j in range(d):
                    #print(j)
                    if self.kbcolors.red[j][i] <= self.r:
                        self.kbcolors.red[j][i] += int(self.r * (1-self.fade))
                        if self.kbcolors.red[j][i] > self.r: self.kbcolors.red[j][i]=self.r
                    if self.kbcolors.green[j][i] <= self.g: 
                        self.kbcolors.green[j][i] += int(self.g * (1-self.fade))
                        if self.kbcolors.green[j][i] > self.g: self.kbcolors.green[j][i]=self.g
                    if self.kbcolors.blue[j][i] <= self.b: 
                        self.kbcolors.blue[j][i] += int(self.b * (1-self.fade))
                        if self.kbcolors.blue[j][i] > self.g: self.kbcolors.blue[j][i]=self.g
                
                
            self.kbcolors.setKeyboardFlat(self.keyboard)
            await asyncio.sleep(self.delay)




    async def changeColor(self,r,g,b):
        self.r=r
        self.g=int(g*0.7)
        self.b=int(b*0.6)
        


