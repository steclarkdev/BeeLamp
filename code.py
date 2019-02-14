import time
import board
import neopixel
import random
from digitalio import DigitalInOut, Direction, Pull

pixel_pin = board.A4
num_pixels = 70
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=1.0, auto_write=False)

RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
WHITE = (25, 25, 25)
BACKCOLOR = (130,130,130)
BEECOLOR = (255,255,0)
speed = 0.01



class Flower:
    modeChangeAgeChange = 20
    modeChangeAge = 0
    modeChangeRnd = 3
    loopCount = 0
    m_stripIndex = 0
    color = BLUE
    birthTime =0

    def __init__(self, time):
        self.modeChangeAge = time
        self.m_stripIndex = random.randint(0,(50-1))

    def stripIndex(self,value,strip):
        calcIndex = self.m_stripIndex+value
        if(calcIndex>=0 or calcIndex <= (num_pixels-1)):
            strip[calcIndex] = self.color

    def update(self,currSec):
        if(self.modeChangeAge < currSec):
            print("Flower rebirth")
            self.m_stripIndex = random.randint(10,50)
            self.modeChangeAge = currSec + self.modeChangeAgeChange + random.randint(-1 * self.modeChangeRnd, self.modeChangeRnd)

    def draw(self,strip):
        strip[self.m_stripIndex] = RED
        self.stripIndex(9,strip)
        self.stripIndex(17,strip)
        self.stripIndex(8,strip)
        self.stripIndex(-9,strip)
        self.stripIndex(-17,strip)
        self.stripIndex(-8,strip)




class Bee:
    mode = 1
    modeChangeAge = 0
    modeChangeAgeChange = 5
    modeChangeRnd = 2
    modeChangeAgeFeed = 10
    loopCount = 0
    FWD = 1
    BACK = 2
    LOOP = 3
    SEEK = 4
    STAY = 5
    m_stripIndex = 0
    birthTime =0
    lastUpdate =0
    fastMove = 0.01
    normalMove = 0.02
    updateLen = normalMove
    baseColor = (50,50,0)
    color = (50,50,0)



    def __init__(self, time):
        self.lastUpdate = time
        self.modeChangeAge = time + self.modeChangeAgeChange

    def stripIndex(self,value):
        self.m_stripIndex += value
        if(self.m_stripIndex  > num_pixels-1):
            self.m_stripIndex = num_pixels-1
        if(self.m_stripIndex < 0):
            self.m_stripIndex = 0

    def update(self,currSec):
        if(self.modeChangeAge < currSec):
            self.mode = random.randint(1,3)
            self.modeChangeAge = currSec + self.modeChangeAgeChange + random.randint(-1 * self.modeChangeRnd, self.modeChangeRnd)
            print("Changed to mode ", self.mode, " with age", self.modeChangeAge)
            seekRnd = random.randint(0,6)
            if(seekRnd == 0):
                self.SEEK = True
                print("Enabled seek")
        if(self.lastUpdate + self.updateLen < currSec):
            #print("Update tick", currSec)
            self.lastUpdate = currSec
            if(self.mode == self.FWD):
                if(self.m_stripIndex >= (num_pixels-1)):
                    self.mode = self.BACK
                self.stripIndex(1)
            if(self.mode == self.BACK):
                if(self.m_stripIndex <= 0):
                    self.mode = self.FWD
                self.stripIndex(-1)
            if(self.SEEK == True):
                for x in range(0,len(flowers)):
                    flower = flowers[x]
                    if(flower.m_stripIndex == self.m_stripIndex):
                        self.modeChangeAge = currSec + self.modeChangeAgeFeed + random.randint(-1 * self.modeChangeRnd, self.modeChangeRnd)
                        self.mode = self.STAY
            if(self.mode == self.STAY):
                #print("Staying")
                self.SEEK = False
                if(self.loopCount == 5):
                   self.loopCount = 0
                if(self.loopCount==0):
                    self.color = (20,20,0)
                if(self.loopCount==1):
                    self.color = (60,60,0)
                if(self.loopCount==2):
                    self.color = (120,120,0)
                if(self.loopCount==3):
                    self.color = (60,60,0)
                if(self.loopCount==4):
                    self.color = (20,20,0)
                self.loopCount += 1
            if(self.mode == self.LOOP):
                self.updateLen = self.fastMove
                if(self.loopCount==6):
                    self.loopCount =0
                    self.updateLen = self.normalMove
                    self.modeChangeAge = currSec
                    return
                if(self.loopCount==0):
                    self.stripIndex(9)
                if(self.loopCount==1):
                    self.stripIndex(17)
                if(self.loopCount==2):
                    self.stripIndex(8)
                if(self.loopCount==3):
                    self.stripIndex(-9)
                if(self.loopCount==4):
                    self.stripIndex(-17)
                if(self.loopCount==5):
                    self.stripIndex(-8)
                self.loopCount = self.loopCount + 1
        #print("Index ", self.m_stripIndex)



buttonL = DigitalInOut(board.BUTTON_A)
buttonL.direction = Direction.INPUT
buttonL.pull = Pull.DOWN
buttonR = DigitalInOut(board.BUTTON_B)
buttonR.direction = Direction.INPUT
buttonR.pull = Pull.DOWN

def showPixel(index,color):
    pixels[index] = color

pixels.fill(BACKCOLOR)


flowersMax = 6
flowers = []
for x in range(flowersMax):
    flower = Flower(time.monotonic())
    flowers.append(flower)

beesMax = 2
bees = []
for x in range(beesMax):
    bee = Bee(time.monotonic())
    bees.append(bee)

while(True):

    if(buttonR.value):
        print("R button")
        bee1.calcXY(1,0)
    if(buttonL.value):
        print("L button")
        bee1.calcXY(-1,0)

    for x in range(0,len(flowers)):
        flower = flowers[x]
        flower.update(time.monotonic())
        flower.draw(pixels)

    for x in range(0,len(bees)):
        bee = bees[x]
        #BACKCOLOR = ( random.randint(22,44), random.randint(22,44), random.randint(22,90))
        showPixel(bee.m_stripIndex,BACKCOLOR)
        bee.update(time.monotonic())
        showPixel(bee.m_stripIndex,bee.color)

    pixels.show()