from neopixel import NeoPixel
from machine import Pin

from math import abs
from math import cos
from math import exp
from math import log
from math import pi
from math import pow
from math import sin
from math import sqrt

class PixelWriter1D(object):

    NULL_FUNCTION = "0"

    def __init__(self, pinNumber, ledCount):
        self.np = NeoPixel(Pin(pinNumber), ledCount)
        self.ledCount = ledCount
        self.rFunc = self.NULL_FUNCTION
        self.gFunc = self.NULL_FUNCTION
        self.bFunc = self.NULL_FUNCTION

    def setRedFunction(self, redFunctionString):
        self.rFunc = redFunctionString

    def setGreenFunction(self, greenFunctionString):
        self.gFunc = greenFunctionString

    def setBlueFunction(self, blueFunctionString):
        self.bFunc = blueFunctionString

    def writeAllPixels(self, t):
        for x in range(self.ledCount):
            self.np[x] = (eval(self.rFunc), eval(self.gFunc), eval(self.bFunc))
        self.np.write()

class PixelWriter2D(PixelWriter1D):

    RASTER = 0
    ZIG_ZAG = 1

    def __init__(self, pinNumber, ledCountX, ledCountY, mode):
        super(PixelWriter2D, self).__init__(pinNumber, ledCountX * ledCountY)
        self.ledCountX = ledCountX
        self.ledCountY = ledCountY
        self.mode = mode

    def writeAllPixels(self, t):
        if self.mode == self.RASTER:
            for x in range(self.ledCountX):
                for y in range(self.ledCountY):
                    self.np[(x * self.ledCountX) + y] = (eval(self.rFunc), eval(self.gFunc), eval(self.bFunc))
        elif self.mode == self.ZIG_ZAG:
            for x in range(self.ledCountX):
                if (x % 2) == 0:
                    for y in range(self.ledCountY):
                        self.np[(x * self.ledCountX) + y] = (eval(self.rFunc), eval(self.gFunc), eval(self.bFunc))
                else:
                    for y in range(self.ledCountY - 1, -1, -1):
                        self.np[(x * self.ledCountX) + (self.ledCountY - (1 + y))] = (eval(self.rFunc), eval(self.gFunc), eval(self.bFunc))

        self.np.write()
