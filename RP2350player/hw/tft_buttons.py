"""
Waveshare 1.3" TFT display with ST7789 controller
"""

from machine import Pin

class Buttons():
    """
    Buttons class for examples, modify for your device.

    Attributes:
        name (str): The name of the device.
        left (Pin): The Pin object representing the left button.
        right (Pin): The Pin object representing the right button.
        fire (Pin): The Pin object representing the fire button.
        thrust (Pin): The Pin object representing the thrust button.
        hyper (Pin): The Pin object representing the hyper button.
    """

    def __init__(self):
        self.name = "gamepi_13"
        self.left = Pin(16, Pin.IN, Pin.PULL_UP) # Joystick left
        self.right = Pin(13, Pin.IN, Pin.PULL_UP) # Joystick right
        self.up = Pin(15, Pin.IN, Pin.PULL_UP) # Joystick up
        self.down = Pin(6, Pin.IN, Pin.PULL_UP) # Joystick 
        self.start = Pin(26, Pin.IN, Pin.PULL_UP) # 
        self.sel = Pin(19, Pin.IN, Pin.PULL_UP) # 

        self.bleft = Pin(9, Pin.IN, Pin.PULL_UP) # button Y (left)
        self.bright = Pin(21, Pin.IN, Pin.PULL_UP) # button A (right)
        self.bup = Pin(5, Pin.IN, Pin.PULL_UP) # button X (up)
        self.bdown = Pin(20, Pin.IN, Pin.PULL_UP) # button B (down
        
        self.tr = Pin(4, Pin.IN, Pin.PULL_UP) # button R
        self.tl = Pin(23, Pin.IN, Pin.PULL_UP) # button L
