import serial
import serial.tools.list_ports
import time

t=time.localtime()
str='ST:{0},{1},{2},{3},{4},{5}'.format(t[0],t[1],t[2],t[3],t[4],t[5])
str='\r\n'+str+'\r\n'
dat = bytes(str, encoding='utf-8')

ser = None
ports = list(serial.tools.list_ports.comports())
for p in ports:
    if 'USB' in p.hwid:
        print(p)
        print(" device       :", p.device)
        print(" name         :", p.name)
        ser = serial.Serial(port=p.device, baudrate=9600, parity='N')
        ser.write(dat) # b'\r\nST:2025,5,1,12,00\r\n')
        data=ser.readline()
        data=data.strip()
        print(data.decode('utf-8'))

"""
    print(p)
    print(" device       :", p.device)
    print(" name         :", p.name)
    print(" description  :", p.description)
    print(" hwid         :", p.hwid)
    print(" vid          :", p.vid)
    print(" pid          :", p.pid)
    print(" serial_number:", p.serial_number)
    print(" location     :", p.location)
    print(" manufactuer  :", p.manufacturer)
    print(" product      :", p.product)
    print(" interface    :", p.interface)
    print("")
"""
    