# built-in
import io
import time
import st7789
import os
import machine
import gc
from machine import Pin, SoftSPI

# components
import tft_config
import sdcard
import globalvalue as g
#from piospi import PioSPI

def startSD():
    # Assign chip select (CS) pin (and start it high)
    cs = machine.Pin(43, machine.Pin.OUT, value=1)

    # Intialize SPI peripheral (start with 1 MHz)
    spi = machine.SPI(id=1,
              baudrate=1_000_000,
              polarity=0,
              phase=0,
              bits=8,
              firstbit=machine.SPI.MSB,
              sck=machine.Pin(30),
              mosi=machine.Pin(31),
              miso=machine.Pin(40))

    # Initialize SD card
    sd = sdcard.SDCard(spi, cs,baudrate=5_000_000)

    # Mount filesystem
    vfs = os.VfsFat(sd)
    try:
        os.mount(vfs, "/sd")
    except:
        pass
    found = False
    for mt in os.mount():
        if mt[1] == "/sd":
            found = True
    if not found:
        print("Error SD")

def startLCD(rotation = 2):
    tft = tft_config.config(rotation) #2 rotation =180)
    tft.init()
    if rotation == 2:
        tft.madctl(0x80)
    g.tft = tft
