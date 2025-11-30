# built-in
import io
import time
import st7789
import os
import machine
import gc
from machine import Pin

# components
import tft_config
import pictview
import watch
import drawMsg
import globalvalue as g
import sdcard
import init
# fonts
import cons32 as font32
import cons48 as font48
import cons64 as font64

last_msgtime = 0
g.weather = None
   
def msg_time():
    global last_msgtime
    rc = 0
    ct = time.gmtime()
    if ct[0] > 2024:
        rc = 1
        if last_msgtime != ct[5]:
            watch.poll()  # Poll COM port
            if ct[0] > 2024:
                drawMsg.showMsg(ct)
            last_msgtime = ct[5]
    return rc

def poll_cmd():
    global last_msgtime
    rc = 0
    ct = time.gmtime()
    if last_msgtime != ct[5]:
        watch.poll() 
        last_msgtime = ct[5]
    return rc
            
def loop():
    global last_msgtime
    last_msgtime = 0
    tft = g.tft
    """
    fps=8
    pictview.pictview("/countdown.tar", 8, tft, None, msg_time)
    """

    while True:
        for d in ("/", "/sd"):
            flist = os.listdir(d)
            for f in flist:
              if f.endswith((".bin",".tar")) is False:
                continue
              if d == '/':
                  outfn = "/" + f
              else:
                  outfn = d+"/"+f
              if g.dbgmsg:
                  print('gc free='+str(gc.mem_free()))
              fps=8

              pictview.pictview(outfn, fps, tft, 0, msg_time)

              gc.collect()
              time.sleep_ms(2000)
              tft.fill(0)

g.dbgtime = False
g.dbgmsg = False
 
button=Pin(26,Pin.IN, Pin.PULL_UP)  #GamePi13 START button
g.button = button
if button.value() == 1:    # skip main() in case of trouble
    init.startSD()
    init.startLCD()
    gc.enable()

    loop()
