"""
GamePi13
SPI driver using PIO0 or 1
"""

import time
import rp2
from machine import Pin, Timer
import machine

# PIO registers
SM_PIO0_NUM = const(0)
SM_PIO1_NUM = const(4)
PIO0_BASE = const(0x50200000)
PIO1_BASE = const(0x50300000)
TXF0 = const(0x010)
RXF0 = const(0x020)
FSTAT = const(0x004)
DREQ_PIO0_TX0 = const(0)
DREQ_PIO0_RX0 = const(4)
DREQ_PIO1_TX0 = const(8)
DREQ_PIO1_RX0 = const(12)

if True:    # use PIO0
    GPIO_ALT = 6
    PIO_BASE_ADDR = PIO0_BASE
    SM_BASE_NUM = SM_PIO0_NUM
    DREQ_PIO_TX = DREQ_PIO0_TX0
    DREQ_PIO_RX = DREQ_PIO0_RX0
else:       # use PIO1
    GPIO_ALT = 7
    PIO_BASE_ADDR = PIO1_BASE
    SM_BASE_NUM = SM_PIO1_NUM
    DREQ_PIO_TX = DREQ_PIO1_TX0
    DREQ_PIO_RX = DREQ_PIO1_RX0

class PioSPI:
    MSB = machine.SPI.MSB
    LSB = machine.SPI.LSB
    sm_init_flag = False
    sm_spi_wr_num = 0
    sm_spi_wr = None

    def __init__(self, **kwargs):
        defaults = {
            "baudrate" : 1_000_000,
            "polarity": 0,
            "phase": 0,
            "bits": 8,
            "firstbit": PioSPI.MSB,
            "sck": None,
            "mosi": None,
            "miso": None,
        }
        #
        self.config = {key: kwargs.get(key, defaults[key]) for key in defaults}

    def init(self, **kwargs):   # change configuration and start/restart SPI
        defaults = self.config
        self.config = {key: kwargs.get(key, defaults[key]) for key in defaults}
        print("init",self.config)
        if PioSPI.sm_init_flag:
            PioSPI.sm_activate(0)
            PioSPI.sm_init_flag = False

        FREQ = self.config["baudrate"] * 4
        PioSPI.stop_pio()
        PioSPI.dump_pio()
        self.sm_start(FREQ)
        PioSPI.dump_pio()
        
        #PioSPI.dma_config(PsramDevice.sm_spi_rd_num, PsramDevice.sm_spi_wr_num)

    def deinit(self):
        pass

    @staticmethod
    def sm_push(value, shft, num):
        if value != 255:
            print("sm_push", value)
        PioSPI.sm_spi_wr.put(value, shft)
        
    @staticmethod
    def sm_pull(num):
        value = PioSPI.sm_spi_wr.get()
        if value != 255:
            print("sm_pull", value)
        return value
        
    def write(self, buf):
        #print("Enter write")
        #print(f"stat:{self.stat_pio():08x}")
        pio_push = PioSPI.pio_push
        pio_pull = PioSPI.pio_pull
        sm_num = PioSPI.sm_spi_wr_num
        #print("len(buf)", len(buf))
        for i in range(len(buf)):
            PioSPI.pio_push(buf[i], 24, sm_num)
            PioSPI.pio_pull(sm_num)

    def write_readinto(self, wbuf, rbuf):
        #print("Enter write_readinto")

        pio_push = PioSPI.pio_push
        pio_pull = PioSPI.pio_pull
        sm_num = PioSPI.sm_spi_wr_num
        for i in range(len(wbuf)):
            PioSPI.pio_push(wbuf[i], 24, sm_num)
            rbuf[i] = PioSPI.pio_pull(sm_num)

    def read(self, nbytes, wchar):
        #print("Enter read")
        buf = bytearray(nbytes)
        pio_push = PioSPI.pio_push
        pio_pull = PioSPI.pio_pull
        sm_num = PioSPI.sm_spi_wr_num
        for i in range(len(buf)):
            PioSPI.pio_push(wchar, 24, sm_num)
            buf[i] = PioSPI.pio_pull(sm_num)

    def readinto(self, buf, wchar):
        #print("Enter readinto")
        pio_push = PioSPI.pio_push
        pio_pull = PioSPI.pio_pull
        sm_num = PioSPI.sm_spi_wr_num
        for i in range(len(buf)):
            PioSPI.pio_push(wchar, 24, sm_num)
            buf[i] = PioSPI.pio_pull(sm_num)


    @micropython.viper
    @staticmethod
    def stat_pio()->int:
       pio = ptr32(uint(PIO_BASE_ADDR))
       return pio[51]

    @micropython.viper
    @staticmethod
    def stop_pio(): # PIO registers to RESET value
       pio = ptr32(uint(PIO_BASE_ADDR))
       pio[0] = 0   # SM_ENABLE = 0
       for i in range(32):
         pio[0x12 + i] = 0  # INSTR_MEM  jmp 0
       for i in range(4):
         pio[0x32 + i * 6] = 0x0001_0000  # CLKDIV (0xc8)
         pio[0x33 + i * 6] = 0x0001_F000  # EXECCTRL
         pio[0x34 + i * 6] = 0x000C_0000  # SHIFTCTRL
         pio[0x37 + i * 6] = 0x1400_0000  # PINCTRL

    @micropython.viper
    @staticmethod
    def dump_pio(): # PIO registers to RESET value
       pio = ptr32(uint(PIO_BASE_ADDR))
       print(f"CTRL     :{pio[0]:08x}")
       print(f"FSTAT    :{pio[1]:08x}")
       for i in range(1):
         print(f"CLKDIV   :{pio[0x32 + i * 6]:08x}")
         print(f"EXECCTRL :{pio[0x33 + i * 6]:08x}")
         print(f"SHIFTCTRL:{pio[0x34 + i * 6]:08x}")
         print(f"ADDR     :{pio[0x35 + i * 6]:08x}")
         print(f"INSTR    :{pio[0x36 + i * 6]:08x}")
         print(f"PINCTRL  :{pio[0x37 + i * 6]:08x}")
       print(f"GPIOBASE :{pio[0x168 // 4]:08x}")
       return
       val = uint(pio[0x37])
       if val & uint(0xe0000000) != uint(0):
           val = uint(pio[0x37])
           val = val & 0x1fffffff
           pio[0x37] = val
           pio[0x37] = pio[0x37] | 0x2000_0000
           print(f"newPINCTRL  :{pio[0x37]:08x}")

    @classmethod
    def sm_activate(cls, flag):
        cls.sm_spi_wr.active(flag)

    @classmethod
    def sm_restart(cls):
        cls.sm_spi_wr.restart()
        

    def sm_start(self, FREQ=2_000_000, force_init = False):
        # PIO definition

        @rp2.asm_pio(sideset_init=(rp2.PIO.OUT_LOW),out_init=rp2.PIO.OUT_HIGH)
        def spi_write_read():
            wrap_target()
            pull().side(0)  # 1
            set(x, 7)       # 2  8bit (byte)
            label("BYTE")
            out(pins, 1).side(0)  # 3
            nop().side(1)   # 4
            in_(pins, 1).side(1)  # 5
            jmp(x_dec, "BYTE").side(0)  # 6
            push().side(0)      #7
            wrap()

        if not PioSPI.sm_init_flag or force_init or PioSPI.stat_pio() == 0x0001f000:
            PioSPI.sm_init_flag = True
            PioSPI.sm_spi_wr_num = SM_BASE_NUM + 0
            rp2.PIO(SM_BASE_NUM // 4).gpio_base(Pin(16))

            self.config["miso"].init(Pin.IN, Pin.PULL_UP)
            self.config["mosi"].init(Pin.IN, Pin.PULL_UP)
            self.config["sck"].init(Pin.IN, Pin.PULL_UP)

            PioSPI.sm_spi_wr = rp2.StateMachine(PioSPI.sm_spi_wr_num)
            PioSPI.sm_spi_wr.init(
                spi_write_read,
                freq=FREQ,
                sideset_base=self.config["sck"],
                out_base=self.config["mosi"],
                in_base=self.config["miso"],
            )
            PioSPI.sm_spi_wr.active(1)

            print(f'freq={FREQ},sideset_base={self.config["sck"]},out_base={self.config["mosi"]},in_base={self.config["miso"]},')
            

    @staticmethod
    @micropython.viper
    def pio_push(byte: uint, shift: int, sm_num: int):
        sm_num = sm_num & 0x03
        dst = ptr32(uint(PIO_BASE_ADDR) + uint(TXF0) + 4 * sm_num)
        stat = ptr32(uint(PIO_BASE_ADDR) + uint(FSTAT))
        mask = 0x010000 << sm_num  # TXFULL
        while stat[0] & mask != 0:  # is FULL
            pass
        dst[0] = byte << shift

    @staticmethod
    @micropython.viper
    def pio_pull(sm_num: int) -> uint:
        sm_num = sm_num & 0x03

        src = ptr32(uint(PIO_BASE_ADDR) + uint(RXF0) + 4 * sm_num)
        stat = ptr32(uint(PIO_BASE_ADDR) + uint(FSTAT))
        mask = 0x0100 << sm_num  # RXEMPTY
        while stat[0] & mask != 0:  # is empty
            pass
        return uint(src[0])
