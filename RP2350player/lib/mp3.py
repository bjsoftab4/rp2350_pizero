from struct import *
import os
import time

import utils

from hw_wrapper import *
from mp3func import Pcm,DecodeMP3

callback_func = None

def mainloop(infile):
    rc = DecodeMP3.prolog(infile, 0, 0, callback_func)

    if rc < 0:
        return
    rc = DecodeMP3.skip_id3v2()
    if rc < 0:
        return
    if not DecodeMP3.mp3file_find_sync_word():
        return
    rc = DecodeMP3.fillfilebuffer()
    if rc < 0:
        return
    rc = DecodeMP3.look_for_1stframe()
    rc = DecodeMP3.getframeinfo(DecodeMP3.decoder, DecodeMP3.frameinfo)
    if rc < 0:
        return

    wait_us = 0
    t_start = time.ticks_ms()
    progress = int(50 * DecodeMP3.fileremain / DecodeMP3.fsize)
    bar = "-" * 50
    if DecodeMP3.callback_func is not None:
        DecodeMP3.callback_func(2, 0)
    
    retc = 0
    lastscan = time.ticks_ms()
    while DecodeMP3.mp3file_find_sync_word():
        rc = DecodeMP3.fillfilebuffer()
        if rc < 0:
           break
        if time.ticks_diff(time.ticks_ms(), lastscan) > 100 and utils.checkKey():
            lastscan = time.ticks_ms()
            st = utils.getKeystring()
            if ' ' in st:
                sec = (DecodeMP3.fsize - DecodeMP3.fileremain) / DecodeMP3.basebr * 8
                #print("sec=",sec)
                if DecodeMP3.mp3seek(sec + 10) < 0:
                    break
            if 'N' in st:
                retc = 4
                break
            if 'P' in st:
                retc = 5
                break
            if 'n' in st:
                retc = 2
                break
            if 'p' in st:
                retc = 3
                break
            if 'q' in st:
                retc = 9
                break
            if ']' in st:
                DecodeMP3.volume += 10
                if DecodeMP3.volume > 255:
                    DecodeMP3.volume = 255
            if '[' in st:
                DecodeMP3.volume -= 10
                if DecodeMP3.volume < 0:
                    DecodeMP3.volume = 0


        lap0 = time.ticks_us()
        while Pcm.get_freebuf() <= len(DecodeMP3.pcmbuf) // 4 // 2:	# get_freebuf returns sample counts
            #print(Pcm.get_freebuf())
            pass
        wait_us += time.ticks_diff(time.ticks_us(), lap0)

        rc = DecodeMP3.part_decode()
        if rc == 1:
            print(bar,end="\r")
            continue
        if rc < 0:
            break

        rc = DecodeMP3.fillfilebuffer()
        if rc < 0:
           break

        p1 = int(50 * DecodeMP3.fileremain / DecodeMP3.fsize)
        if p1 != progress:
            progress = p1
            print("+",end="")
            if DecodeMP3.callback_func is not None:
                DecodeMP3.callback_func(2, 100 - progress * 2)
    Pcm.stop()
    utils.waitKeyOff()
    print("")
    total_ms = time.ticks_ms() - t_start
    #print(f"wait_ms={int(wait_us/1000)}, total_ms={total_ms}, CPU LOAD={100-int(wait_us/10/total_ms)}%")
    return retc

def run(fdir = "/sd", callback = None):
    global callback_func
    callback_func = callback
    
    Pcm.init(PCM_GPIO)
    rc = -1
    try:
        rc = utils.scan_dir(fdir, mainloop)
    finally:
        DecodeMP3.callback_func = None
        print("close")
        Pcm.deinit()
        os.listdir("/")
    return rc
