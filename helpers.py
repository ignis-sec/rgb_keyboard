
def rgb_to_hid_buf(r,g,b, id=1):
    """ Convert RGB colors to HID message buffer
    """
    if(id>8):
        return False
    return b"\x00\x14\x00" + bytes([id,r,g,b]) + b"\x00\x00"

def mode_to_hid_buf(mode=b"\x00\x00", speed=0, brightness=32, coloring_scheme=1,rotation=0,c=0):
    """ Convert lighting mode to HID message buffer
    """
    return b"\x00\x08\x02" + mode + bytes([speed,brightness,coloring_scheme,rotation,c])