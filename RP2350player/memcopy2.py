@micropython.viper
def bmp_double(dst:ptr16, src:ptr16, width:int, height:int):
    wlimit = width
    hlimit = height
    if wlimit > 120:
        wlimit = 120
    if hlimit > 90:
        hlimit = 90
        
    for y in range(hlimit):
        spos = (y * width)
        dpos = (y * 2 * 120 * 2)
        
        for i in range(wlimit):
            d1 = src[spos]
            dst[dpos] = d1
            dst[dpos+1] = d1
            dst[dpos+240] = d1
            dst[dpos+241] = d1
            spos += 1
            dpos += 2
"""
@micropython.native
def bmp_double(dst, src, width, height):
    wlimit = width
    hlimit = height
    if wlimit > 120:
        wlimit = 120
    if hlimit > 120:
        hlimit = 120
        
    for y in range(hlimit):
        spos = y * width
        dpos = y * 2 * 120 * 2
        
        spos *= 2
        dpos *= 2
        for i in range(wlimit):
            d1 = src[spos]
            d2 = src[spos+1]
            dst[dpos] = d1
            dst[dpos+1] = d2
            dst[dpos+2] = d1
            dst[dpos+3] = d2
            dst[dpos+120*4] = d1
            dst[dpos+120*4+1] = d2
            dst[dpos+120*4+2] = d1
            dst[dpos+120*4+3] = d2
            spos += 2
            dpos += 4
"""
