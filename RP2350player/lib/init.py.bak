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
import sdcard
import globalvalue as g

def startSD():
    # Assign chip select (CS) pin (and start it high)
    cs = machine.Pin(21, machine.Pin.OUT)

    # Intialize SPI peripheral (start with 1 MHz)
    spi = machine.SPI(id=0,
                      baudrate=10000000,
                      polarity=0,
                      phase=0,
                      bits=8,
                      firstbit=machine.SPI.MSB,
                      sck=machine.Pin(18),
                      mosi=machine.Pin(19),
                      miso=machine.Pin(20))

    # Initialize SD card
    sd = sdcard.SDCard(spi, cs)

    # Mount filesystem
    vfs = os.VfsFat(sd)
    os.mount(vfs, "/sd")
#    print(os.listdir("/sd"))

def startLCD():
    tft = tft_config.config(2)
    tft.init()
    tft.madctl(0x80)
    g.tft = tft
