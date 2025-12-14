import io
import time
import st7789
import memcopy2
import cons48 as font48
import cons32 as font32
import globalvalue as g
import vga1_16x32 as font16
import vga2_8x8 as font8

screen = bytearray(240*180*2)
def pictview(outfn, fps, tft, fill=0, callback=None):
    global screen
    bmp2=screen
    if fill != None:
        tft.fill(fill)
    waitms=int(1000/fps)
    try:
        fi = io.open(outfn, mode='rb')
    except:
        return
    if g.dbgmsg:
        print(outfn)
    for i in range(3600):
        if g.button.value() == 0:
            break
        
        last = time.ticks_ms()    
        if callback != None:
            rc = callback()
        else:
            rc = 0
        if rc == 0:
             tft.text(font16, 'T='+str(int(i/fps))+"."+str(int(i%fps))+" ", 0, 180)
             tft.text(font16, outfn, 0, 208)


        if outfn.endswith('.bin'):
            buf = fi.read(6) # read size of jpeg data
            if len(buf) == 0:
                break  # EOF
            sz = int(buf.decode(), 16)
            buf = fi.read(sz)
            if len(buf) != sz:
                break  # EOF or bad data
        elif outfn.endswith('.tar'):
            buf = fi.read(512) # read tar header
            if len(buf) != 512:
                break  # ERROR
            fn=buf[0:100].rstrip(b"\0").decode()
            if g.dbgmsg:
                print(fn)
            if len(fn) == 0:
                break  # EOF
            sz = int(buf[0x7c:0x87].decode(),8)
            if g.dbgmsg:
                print(sz)
            if (sz % 512) != 0:
              sz += 512 - sz % 512
            if fn.endswith((".jpg",".jpeg")) is False:
                fi.seek(sz,1)
                continue
            buf = fi.read(sz)
            if len(buf) != sz:
                break  # EOF or bad data
        else:
            break
        
        jpginfo = tft.jpg_decode(buf)

        bmp1 = jpginfo[0]
        w =jpginfo[1]
        h =jpginfo[2]
        memcopy2.bmp_double(bmp2, bmp1, w, h)

        hlim = h * 2
        hofst = 0
        if hlim > 180:
            hlim = 180
        if hlim < 180:
            hofst = int((180 - hlim) /2)
        tft.blit_buffer(bmp2, 0, hofst, 240, hlim)

        dif = time.ticks_ms() - last
        if( dif < waitms):
            time.sleep_ms(waitms - dif)
        if g.dbgtime:
          print(dif)

    fi.close()

