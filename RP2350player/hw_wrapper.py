""" wrapper for GamePi13 """
PCM_GPIO = (18,19) # for GamePi13
#PCM_GPIO = (26,27)	# for picocalc
import time

class picocalc:
    keyboard, display = None, None

class KeyFunc:
    #import picocalc
    import tft_buttons
    button=tft_buttons.Buttons()
    #keyb = picocalc.keyboard
    @classmethod
    def waitKeyOff(cls):
        time.sleep_ms(100)
        while cls.checkKey():
            st = cls.getKeystring()
            time.sleep_ms(200)

    @classmethod
    def checkKey(cls):
        button = cls.button
        if button.right.value() == 0:
            return True
        if button.up.value() == 0:
            return True
        if button.down.value() == 0:
            return True
        if button.left.value() == 0:
            return True
        if button.bright.value() == 0:
            return True
        if button.bup.value() == 0:
            return True
        if button.bdown.value() == 0:
            return True
        if button.bleft.value() == 0:
            return True
        if button.start.value() == 0:
            return True
        if button.select.value() == 0:
            return True

        return False

    @classmethod
    def getKeystring(cls):
        button = cls.button
        if button.right.value() == 0:
            return "n"
        if button.up.value() == 0:
            return "u"
        if button.down.value() == 0:
            return " "
        if button.left.value() == 0:
            return "p"
        if button.bdown.value() == 0:
            return "["
        if button.bup.value() == 0:
            return "]"
        if button.start.value() == 0:
            return "s"
        if button.select.value() == 0:
            return "S"
        return ""


class PicoJpeg:
    tft = None

    @classmethod
    def start(cls, mode=None):
        import globalvalue as g
        cls.tft = g.tft
        return

    @classmethod
    def end(cls):
        return

    @classmethod
    def getinfo(cls, buf):
        return cls.tft.jpgdec_init(buf)

    @classmethod
    def decode_core(cls, buf, mode, core, offset=None):
        rc = cls.tft.jpgdec_decodex2(buf)
        return rc

    @classmethod
    def clear(cls):
        return cls.tft.fill(0)

    # dummy modules
    @classmethod
    def decode_opt(cls, buf, offset, crop, ioption):
        return (0,0,0)


    @classmethod
    def decode_split(cls, fsize, buf, offset, crop, ioption):
        return (0,0,0)

    @classmethod
    def decode_core_wait(cls, force=None):
        return (0,0)

    @classmethod
    def decode_split_wait(cls):
        return (0,0,0)

    @classmethod
    def decode_split_buffer(cls, bufnum, newpos, buf):
        return (0,0,0)

