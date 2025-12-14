# test jpeg draw functions

import io
import time
import gc
import os
from jpegfunc import JpegFunc
from mp3 import Pcm
import utils
from hw_wrapper import *

wmax=320
hmax=320


class MyException(Exception):
    pass
import gc


def play_movie(fname):
    return JpegFunc.play_movie3(fname, fname)
    
def run(fdir = "/sd"):
    global screen
    utils.waitKeyOff()
    print("Enter main")
    try:
        JpegFunc.start()
        Pcm.init(PCM_GPIO)	#for GamePi13
        utils.scan_dir(fdir, play_movie, (".tar"))
        #for fname in ("/sd/eva01.tar","/sd/GQXOP.tar"):
        #    rc = JpegFunc.play_movie3(fname, fname)
        #    waitKeyOff()
    finally:
        print("Leave main")
        JpegFunc.end()
        Pcm.deinit()

import globalvalue as g
g.dbgtime = True
g.dbgmsg = False

import sdcard
import init
init.startSD()
init.startLCD()

if __name__ == "__main__":
    run()

