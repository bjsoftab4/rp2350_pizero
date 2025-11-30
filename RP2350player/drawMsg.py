import io
import time
import pictview
#import vga1_16x16 as font16
# import vga1_16x32 as font32
#import cons32 as font32
import cons32 as font32
import cons48 as font48
import cons64 as font64
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
