# RGB Keyboard Interface

Usage: `rgb_keyboard.py [-h] [-v] [-m MODE] [-s SPEED] [-r ROTATION] [-b BRIGHTNESS] [-c [COLOR [COLOR ...]]]`

```
RGB Keyboard CLI

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Set verbosity level
  -m MODE, --mode MODE  Lighting Mode
  -s SPEED, --speed SPEED
                        Effect speed
  -r ROTATION, --rotation ROTATION
                        Effect rotation
  -b BRIGHTNESS, --brightness BRIGHTNESS
                        Effect brightness
  -c [COLOR [COLOR ...]], --color [COLOR [COLOR ...]]
                        RGB color, id#rrggbb, hex. Id is between 1-7
```

## Tested Platforms
For now, only windows. This project uses pywinusb, and ctypes for dll loading. For Mac/Linux, you can check out [avell unofficial control center](https://github.com/rodgomesc/avell-unofficial-control-center) by [Rodrigo Gomes](https://github.com/rodgomesc) or [my fork of that project](https://github.com/FlameOfIgnis/avell-unofficial-control-center)

## Example - Default modes

These are the modes supported by firmware, and after setting the mode, script will exit (but effect will continue)

- Set keyboard to default effect (rainbow wave)
`python3 rgb_keyboard.py`

- Set keyboard to rainbow wave, but slower
`python3 rgb_keyboard.py -m WAVE -s 3`


### Supported Modes:

Supported modes are taken from the LightingMode class:
```python
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
```

## Example - Extended modes
This module allows writing extended effects. One example included in the module is RAINBOW_FADE, and MUSIC.

`python3 rgb_keyboard.py -m RAINBOW_FADE`

This will invoke rainbow_fade function from RGBRenderer class.
```python
def rainbow_fade(self):
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
```

`python3 rgb_keyboard.py -m MUSIC`


## Adding New Effects

Adding new effects are fairly easy. You just need to implement the animation of colors on `KeyboardMatrix`, and call `KeyboardMatrix.render()` for each frame.

Then, all you need to do is add your function name and identifier to `ExtendedModes` class in `lighting_modes.py`

You can extend the RGBRenderer class, but feel free to fork this project, add the function to the RGBRenderer class and send a pull request!



















