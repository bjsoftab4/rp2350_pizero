import io
import time

import vga1_16x32 as font32
import cons48 as font48
import cons64 as font64
import vga1_8x8 as font8
import vga1_16x16 as font16
import watch
import globalvalue as g


last_msgtime = 0
def showMsg(ct):
    if ct[0] > 2024:
        tft = g.tft
        str0="{:02d}/{:02d}".format(ct[1], ct[2])
        str1="{:02d}:{:02d}".format( ct[3], ct[4])
        str2=":{:02d}".format(ct[5])
        tft.write(font64, str1, 0, 240-60)
        
        if g.weather == None:
            tft.write(font48, str0, 160, 240-48)
        else:
            idx = int(ct[5]/3) % len(g.weather)
            if ct[5] % 3 == 0:
                tft.fill_rect(160,240-48,80,48,0)
                tft.write(font48, g.weather[idx], 160, 240-48)

def showMsg48(msg, x, y):
    tft = g.tft
    tft.fill_rect(x,y,240,48,0)
    tft.write(font48, msg, x, y)
    
def showMsg32(msg, x, y):
    tft = g.tft
    tft.fill_rect(x,y,240,32,0)
    tft.text(font32, msg, x, y)

def showMsg8(msg, x, y):
    tft = g.tft
    tft.fill_rect(x,y,240,8,0)
    tft.text(font8, msg, x, y)

def showMsg16(msg, x, y):
    tft = g.tft
    tft.fill_rect(x,y,240,16,0)
    tft.text(font16, msg, x, y)

