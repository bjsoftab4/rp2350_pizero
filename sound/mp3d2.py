from struct import *
import os
import time

import sound
import picocalc
from picojpeg import PicoJpeg
def checkKey():
    global keyb
    kc = keyb.keyCount()
    if kc == 0:
        return False
    return True

def getKeystring():
    global keyb
    kc = keyb.keyCount()
    if kc == 0:
        return ""
    buf = bytearray(kc+1)
    keyb.readinto(buf)
    st = buf.rstrip(b"\0").decode()
    return st

MAX_NGRAN = 2
MAX_NCHAN = 2
MAX_NSAMP = 576
MAX_BUFFER_LEN=(MAX_NSAMP * MAX_NGRAN * MAX_NCHAN)
ERR_MP3_NONE = 0
class Pcm:
    @classmethod
    def init(cls):
        sound.pcm_init()
    
    @classmethod
    def deinit(cls):
        sound.pcm_deinit()
    
    @classmethod
    def setbuffer(cls,addr):
        sound.pcm_setbuffer(addr)
    
    @classmethod
    def setfreq(cls,f):
        sound.pcm_setfreq(f)
    
    @classmethod
    def start(cls):
        sound.pcm_start()
    
    @classmethod
    def stop(cls):
        sound.pcm_stop()
        
    @classmethod
    def get_freebuf(cls):
        return sound.pcm_get_freebuf()
    
    @classmethod
    def push(cls,addr,mode):
        return sound.pcm_push(addr,mode)   
    
    
class DecodeMP3:
    pcmbuf = memoryview(bytearray(MAX_BUFFER_LEN * 2 * 10))
    pcmlen = len(pcmbuf)//4
    
    filedata1 = bytearray(4096)
    filedata2 = bytearray(4096)

    stream = memoryview(filedata1)
    stream_ptr = 0
    stream_end = 0
    stream_flag = 1

    @classmethod
    def BYTES_LEFT(cls):
        return cls.stream_end - cls.stream_ptr
        
    @classmethod
    def READ_PTR(cls):
        return cls.stream_ptr

    @classmethod
    def CONSUME(cls, n):
        cls.stream_ptr += n

    @classmethod
    def skip_id3v2(cls):
        if cls.BYTES_LEFT() < 10:
            return

        data = cls.stream[cls.READ_PTR():]
        if not ( data[0] == 0x49 and
            data[1] == 0x44 and
            data[2] == 0x33 and
            data[3] != 0xff and
            #data[4] != 0xff and
            (data[5] & 0x1f) == 0 and
            (data[6] & 0x80) == 0 and
            (data[7] & 0x80) == 0 and
            (data[8] & 0x80) == 0 and
            (data[9] & 0x80) == 0):
                #print(f"NO id3v2")
                return
        
        size = (data[6] << 21) | (data[7] << 14) | (data[8] << 7) | (data[9])
        size += 10 # size excludes the "header" (but not the "extended header")
        cls.CONSUME(size)
        print(f"skip_id3v2:{size + 10}bytes")

    @classmethod
    def mp3file_find_sync_word(cls):
        offset = sound.mp3findsyncword(cls.stream[cls.READ_PTR():], cls.BYTES_LEFT())
        if offset >= 0:
            cls.CONSUME(offset)
            return True
        return False
    """
    typedef struct _MP3FrameInfo {
        int bitrate;
        int nChans;
        int samprate;
        int bitsPerSample;
        int outputSamps;
        int layer;
        int version;
    } MP3FrameInfo;
    """
    @classmethod
    def print_frameinfo(cls, frameinfo):
        #print(frameinfo)
        rc = unpack("<LLLLLLL", frameinfo)
        print(rc)
        bitrate, nchans, samprate, bitspersample, outputsamps, layer, version = rc
        
        #bitrate, nchans, samprate, bitspersample, outputsamps, layer, version = unpack_from("<i", frameinfo)
        print(f"bitrate={bitrate}, nchans={nchans},samprate={samprate},bitspersample={bitspersample},outputsamps={outputsamps},layer={layer},version={version}")

    @classmethod
    def hexdump(cls, buf, title=""):
        print(title)
        for i in range(32):
            print(buf[i],end=" ")
        print("")
        
    @classmethod
    def main(cls, infile):
        print(infile)
        fs = 44000
        delay = int(1_000_000 / fs)
        MIN_FILE_BUF_SIZE = 1044

        decoder = sound.mp3initdecoder()
        fi = open(infile, "rb")
        fsize = fi.seek(0, 2)  # os.SEEK_END
        fi.seek(0, 0)  # os.SEEK_SET
        fleft = fsize

        cls.stream_end = len(cls.stream) #fsize
        cls.stream_ptr = 0

        fi.readinto(cls.stream)
        fleft -= len(cls.stream)
        print(f"fleft={fleft}")
        frame=0
        frameinfo = memoryview(bytearray(32))
        audiobuf = memoryview(bytearray(MAX_BUFFER_LEN * 2))

        Pcm.setbuffer(memoryview(cls.pcmbuf))
        Pcm.setfreq(44100)
        Pcm.start()
        pcmbufx = memoryview(bytearray(MAX_BUFFER_LEN * 2 * 2))
        wait_us = 0
        t_start = time.ticks_ms()
        progress = int(50 * fleft / fsize)
        bar = "|"
        for i in range(51):
            bar += " "
        bar += "|"
        bytes_max = 0
        
        cls.skip_id3v2()
        if cls.BYTES_LEFT() < 0:
            print("skip_id3v2 overrun", cls.BYTES_LEFT())
            rc = fi.seek(-cls.BYTES_LEFT(), 1)
            print("seek pos=",rc)

            fleft -= -cls.BYTES_LEFT()
            rc = fi.readinto(cls.stream)
            fleft -= len(cls.stream)
            if rc <=0:
                print("EOF")
                return
            cls.stream_ptr = 0
            cls.stream_end = len(cls.stream)

        while cls.mp3file_find_sync_word():
            if checkKey():
                Pcm.stop()
                break
            cls.skip_id3v2()
            if cls.BYTES_LEFT() < 0:
                print("skip_id3v2 overrun", cls.BYTES_LEFT())
                rc = fi.seek(-cls.BYTES_LEFT(), 1)
                print("seek pos=",rc)
                fleft -= -cls.BYTES_LEFT()
                rc = fi.readinto(cls.stream)
                fleft -= len(cls.stream)
                if rc <=0:
                    print("EOF")
                    break
                cls.stream_ptr = 0
                cls.stream_end = len(cls.stream)
            #print(fi)
            err = sound.mp3getnextframeinfo(decoder, frameinfo, cls.stream[cls.READ_PTR():]);
            if err != ERR_MP3_NONE:  #BUG バッファが4バイト未満の時もエラーになる
                cls.hexdump(cls.stream[cls.READ_PTR():], "frameinfo")
                print("It may be VBR  MP3GetNextFrameInfo rc=", err)
                break
            rc = unpack("<LLLLLLL", frameinfo)
            bitrate, nchans, samprate, bitspersample, outputsamps, layer, version = rc
            if fs != samprate / 1:
                fs = samprate / 1
                delay = int(1_000_000 / fs)
                MIN_FILE_BUF_SIZE = int(27 * bitrate / 8000)
                print(MIN_FILE_BUF_SIZE)
                #sound.reopen(delay, nchans)
                cls.print_frameinfo(frameinfo)
                print(f"fs={fs}, delay={delay}")
                Pcm.stop()
                Pcm.setfreq(samprate)
                Pcm.start()
                print(bar)

            #cls.print_frameinfo(frameinfo)
            #print(fi)
            bytes_left = cls.BYTES_LEFT()
            inbuf = cls.stream[cls.READ_PTR():]
            #print("stream len", len(cls.stream), bytes_left)
            #print("inbuf len", len(inbuf))
            #print("audiodata len", len(audiodata))
            #break
            if False: #bytes_left < MIN_FILE_BUF_SIZE:
                cls.stream[0:bytes_left] = inbuf[0:bytes_left]
                rc = fi.readinto(cls.stream[bytes_left:])
                fleft -= rc
                cls.stream_ptr = 0
                cls.stream_end = len(cls.stream)
                bytes_left = cls.BYTES_LEFT()
                inbuf = cls.stream[cls.READ_PTR():]
                
            rc = sound.mp3decode(decoder, inbuf, bytes_left, audiobuf, 0)
            if bytes_max < bytes_left - rc:
                    bytes_max = bytes_left - rc
                    print("bytes_max",bytes_max)

            if rc <= 0:
                #print("mp3decode rc=",rc)
                cls.stream[0:bytes_left] = inbuf[0:bytes_left]
                rc = fi.readinto(cls.stream[bytes_left:])
                fleft -= len(cls.stream)
                #print(f"fleft={fleft}")
                if rc <=0:
                    print("EOF")
                    break
                cls.stream_ptr = 0
                cls.stream_end = len(cls.stream)
                bytes_left = cls.BYTES_LEFT()
                inbuf = cls.stream[cls.READ_PTR():]
                rc = sound.mp3decode(decoder, inbuf, bytes_left, audiobuf, 0)
                if rc < 0:
                    print("give up")
                    break
            #print(cls.pcmflag, sound.dma_getcount(), outputsamps)
            if False:
                if nchans == 2:
                    sound.mp3pcm2dma(audiobuf[0:outputsamps * 2], pcmbufx,0)
                else:
                    sound.mp3pcm2dma(audiobuf[0:outputsamps * 2], pcmbufx,1)
                #cls.hexdump(memoryview(pcmbufx), "pcmbufx")
            lap0 = time.ticks_us()
            while Pcm.get_freebuf() <= outputsamps * 4:
                # print(Pcm.get_freebuf())
                pass
            wait_us += time.ticks_diff(time.ticks_us(), lap0)
            if False:
                if nchans == 2:
                    left = Pcm.push(pcmbufx[0:outputsamps * 2], 0)
                else:
                    left = Pcm.push(pcmbufx[0:outputsamps * 4], 0)
            left = Pcm.push(audiobuf[0:outputsamps * 2], nchans)
            if( left != 0):
                print("left=",left)
    
            #rc = sound.mp3decode(decoder, inbuf, bytes_left, audiodata, 0);
            #print(rc)
            cls.CONSUME(cls.BYTES_LEFT() - rc)
            p1 = int(50 * fleft / fsize)
            if p1 != progress:
                progress = p1
                print("x",end="")
        print("")
        print(f"wait_ms={int(wait_us/1000)}, total_ms={time.ticks_ms() - t_start}")
fs = 11000
#delay = 1_000_000 / 44100
delay = int(1_000_000 / fs)
keyb = picocalc.keyboard
#sound.open(delay)
while checkKey():
    st = getKeystring()
    time.sleep_ms(100)
Pcm.init()
fdir = "/sd/mp3-0"
#fdir = "/"
flist = os.listdir(fdir)
flist.sort()
try:
    i = 0
    while i < len(flist):
        fn = flist[i]
        if fn.endswith(".mp3"):
           DecodeMP3.main(fdir +"/" + fn)
        if checkKey():
            st = getKeystring()
            if 'q' in st:
                rc = -1
                break
            if 'p' in st:
                i = i - 1
                if( i < 0):
                    i = 0
                continue
        time.sleep_ms(100)
        while checkKey():
            st = getKeystring()
        i+=1
finally:
    print("close")
    Pcm.deinit()
    