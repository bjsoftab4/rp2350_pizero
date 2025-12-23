# built-in
import io
import time
import st7789
import os
import machine
import gc
from machine import Pin
import sys

sys.path.append("/hw")
# components
# common 
import sdcard
import utils
from jpegfunc import JpegFunc
from mp3func import Pcm,DecodeMP3
import mp3

# gamepi
import tft_config
import watch
import drawMsg
import globalvalue as g
import init
from hw_wrapper import *


last_msgtime = 0
g.weather = None

def msg_mp3(cmd, para1):
    msg_time()
    if cmd == 1:   #MP3 info
        dirname, filename = para1.rsplit("/", 1)
        drawMsg.showMsg32(dirname, 0, 0)
        drawMsg.showMsg32(filename, 0, 32)
        return
    if cmd == 2:   #progress
        ll = para1 // 4
        bar = "!" * ll + "." * (25 - ll)
        msg = f"{bar}"
        drawMsg.showMsg8(msg, 0, 120)
        return
    if cmd == 3:   #MP3 info
        drawMsg.showMsg32(para1, 0, 80)
        return
    
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
    else:
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

    tft.fill(0)

    def mp3run(fdir = "/sd"):
        tft.fill(0)
        rc = mp3.run(fdir, msg_mp3)
        tft.fill(0)
        return rc

    def play_func(fname):
        JpegFunc.x2 = True
        return JpegFunc.play_movie3(fname, fname, msg_time)

    def play_func_no_sound(fname):
        JpegFunc.x2 = True
        return JpegFunc.play_movie3(fname, None, msg_time)

    def mjrun(fdir = "/sd", soundflag = False):
        utils.waitKeyOff()
        try:
            rc = -1
            JpegFunc.start()
            if soundflag:
                Pcm.init(PCM_GPIO)	#for GamePi13
            if soundflag:
                rc = utils.scan_dir(fdir, play_func, (".tar"))
            else:
                rc = utils.scan_dir(fdir, play_func_no_sound, (".tar"))
        finally:
            print("Leave mjrun")
            JpegFunc.end()
            if soundflag:
                Pcm.deinit()
        return rc
        
    while True:
        while True:
            rc = -1
            for d in ("/sd"):
                rc = mjrun(d, False)
                if rc < 0 or rc == 9:
                    break
            gc.collect()
            if rc == 9:
                break
            
        while True:
            rc = -1
            for d in ("/sd"):
                rc = mjrun(d, True)
                if rc < 0 or rc == 9:
                    break
            gc.collect()
            if rc == 9:
                break
        while True:
            rc = -1
            for d in ("/sd"):
                rc = mp3run(d)
                if rc < 0 or rc == 9:
                    break
            gc.collect()
            if rc == 9:
                break


g.dbgtime = False
g.dbgmsg = False
button=Pin(26,Pin.IN, Pin.PULL_UP)  #GamePi13 START button
g.button = button

if button.value() == 1:    # skip main() when pressing START
    for _ in range(3):
        try:
            init.startSD()
            break
        except:
            print("SD error, retry")
            time.sleep(1)
    init.startLCD(0)    # 0:normal 2:mirror
    gc.enable()
    loop()
