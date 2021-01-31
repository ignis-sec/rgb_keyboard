
import math
import asyncio
from .audio_loopback.audio_loopback import AudioController
from .audio_loopback.audio_visualizer import AudioVisualizer2D

class KeyboardAudioVisualizer(AudioVisualizer2D):
    """ Audio visualizer class for keyboard.
        convert audio data to color_matrix
    """
    def __init__(self, color_matrix, audio_controller=None, ceiling=120, fade=0.8, delay=0, ambient_brightness_coef=0.1, dampen=0, dampen_bias=0.98, ceiling_bias=0.985):
        super().__init__(color_matrix, audio_controller, ceiling, fade, delay, ambient_brightness_coef, dampen, dampen_bias, ceiling_bias)
        
    def visualize(self, row=25,col=2, top=200):
        return super().visualize(row=row)

