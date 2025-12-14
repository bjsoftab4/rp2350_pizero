import sound
import io
import time
import math
from struct import *
#fs = 44100
fs = 22000
#delay = 1_000_000 / 44100
delay = int(1_000_000 / fs)

def makewav16(freq):
    """
    samples = fs / freq
    """
    samples = int(fs / freq )
    buf=bytearray(samples * 200)
    for i in range(samples * 100):
        deg = 360 * i / samples
        v = math.sin(math.radians(deg))
        v16 = int(v * 30000) // 64 + 1024
        pack_into("<H", buf, i*2, v16)
    return buf

def makewav8(freq):
    """
    samples = fs / freq
    """
    samples = int(fs / freq )
    buf=bytearray(samples)
    for i in range(samples):
        deg = 360 * i / samples
        v = math.sin(math.radians(deg))
        #print(v)
        buf[i] = int(v * 120) + 128
    return buf    
def make1(fbuf):    
    v = 0
    stp=50
    ud = stp
    for i in range(len(fbuf) // 2):
        fbuf[i+i] = 0
        fbuf[i+i+1] = v
        v = v + ud
        if v > 127:
            v = 127
            ud = -stp
        if v < 0:
            v = 0
            ud = stp
    
def unpackbuf(wavbuf, fbuf):
    for i in range(len(fbuf) / 2):
        #print(i)
        val = unpack_from("<h", fbuf, i*2)
        #print(i,val[0])
        wavbuf[i] = int(val[0] // 256) + 128
   
def make2(wavbuf, fbuf):    
    for i in range(len(wavbuf)):
        val = (fbuf[i+i+1] << 8) | fbuf[i+i]
        val0 = val
        if val >= 0x8000:
            val = -(0x10000 - val)
        val = val // 64
        if val > 127:
            val = 127
        if val < -127:
            val = -127
        val = val + 128
        wavbuf[i] = val
        if val != 0:
        #    print(val0, val, end=" ")
            pass

#wavbuf=bytearray(4096*4)
#fbuf=bytearray(8192*4)

wbuf = makewav16(440)

#wavbuf=bytearray(len(buf)//2)
#unpackbuf(wavbuf, buf)
#for i in range(len(wbuf)):
#    print(wbuf[i])

#for i in range(5000):
fi = open("/sd/kousen.bin", "rb")
buf = bytearray(40960)
fi.readinto(buf)
"""
for i in range(len(buf) / 2):
    #print(i)
    val = unpack_from("<h", buf, i*2)
    #print(i,val[0])
    pack_into("<h", buf, i * 2, val[0] // 32 + 1024)
"""

pcmbuf = memoryview(bytearray(81920))
sound.mp3pcm2dma(buf, pcmbuf, 0)

print(len(buf))   
sound.dma_play(pcmbuf, 11000)

while True:
    print(sound.dma_getcount())
    if fi.readinto(buf) <= 0:
        break
    while sound.dma_getcount() >= 10240:
        pass
    sound.mp3pcm2dma(buf, pcmbuf, 0)

    print(sound.dma_getcount())
    if fi.readinto(buf) <= 0:
        break
    while sound.dma_getcount() < 10240:
        pass
    sound.mp3pcm2dma(buf, pcmbuf[40960:], 0)
sound.dma_end()
time.sleep_us(1)

if False:
    sound.open(23)
    fbuf1 = bytearray(8192)
    fbuf2 = bytearray(8192)
    sound.open(delay)
    fi = open("/sd/kousen.bin", "rb")
    try:
        while True:
            rc = fi.readinto(fbuf1)
            if rc <= 0:
                break
            while sound.testbuff() < 3:
                pass
            sound.addbuff(fbuf1)
            
            rc = fi.readinto(fbuf2)
            if rc <= 0:
                break
            while sound.testbuff() < 3:
                pass
            sound.addbuff(fbuf2)
    finally:
        print("close")
        sound.close()
