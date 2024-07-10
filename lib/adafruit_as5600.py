import time
import board
from adafruit_bus_device.i2c_device import I2CDevice

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_AS5600.git"

_AS5600_ADDR = 0x36
_REG_ANGLE = 0x0E

class AS5600:
    def __init__(self, i2c, address=_AS5600_ADDR):
        self.i2c_device = I2CDevice(i2c, address)
        self.buffer = bytearray(2)

    @property
    def angle(self):
        with self.i2c_device:
            self.i2c_device.write_then_readinto(bytearray([_REG_ANGLE]), self.buffer)
        angle = (self.buffer[0] << 8) | self.buffer[1]
        return angle