import sys
import uselect
import time
import machine
import globalvalue as g

spoll = uselect.poll()
spoll.register(sys.stdin, uselect.POLLIN)
g.weather_msg = ''
g.weather_icon=''

def analyze(line):
    if line == None:
        return
    cmd = ''
    try:
        cmd = line.split(':')[0]
        param = line.split(':')[1]
    except:
        pass
    if cmd == 'ST':
        # param should be "ST:2025,5,29,14, 59)  2025/5/29 14:59:00.0
        dt = tuple(map(int,param.split(',')))
        dt = (dt[0],dt[1],dt[2],0,dt[3],dt[4],dt[5],0)
        machine.RTC().datetime(dt)
        print(time.gmtime())

    if cmd == 'WEATHER':
        dt = tuple(param.split(','))
        print(dt)
        g.weather = dt

def watch_serial():
    if not spoll.poll(0):
        return None
        
    line = sys.stdin.readline()
    line = line.replace('\n', '')
    line = line.replace('\r', '')
    if len(line) == 0:
        return None
    return line

def poll():
        ans = watch_serial()
        analyze(ans)

def test():
    while True:
        ans = watch_serial()
        if ans != None:
            print("data:"+ans)
            print("size=",len(ans))
        else:
            print("Nodata")
            
 #       time.sleep_ms(1000)
        analyze(ans)
