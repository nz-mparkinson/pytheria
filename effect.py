#!/usr/bin/python

#Import libraries
from node import *

#Define an Enum for EffectType
class EffectType(Enum):
    HEALTH_BAR = 1
    EXPLOSION = 2
    IMPLOSION = 3
    VERTICAL = 4  #TODO square that grows vertically, looses opacity

#Define a class for Effect
class Effect(Node):
    EFFECT_TIME = 3
    IMAGE_EXPLOSION = "../resources/mine/circle.png"
    IMAGE_HEALTH_BAR = "../resources/mine/healthbar.png"
    SIZE_MOD_EXPLOSION = 5
    TIME_EXPLOSION = 0.2
    TIME_IMPLOSION = 0.5
    TIME_HEALTH_BAR = 3
    TRANSPARENCY_EXPLOSION = 150

    #Define the constructor
    def __init__(self, width, height, posX, posY, imageString, type):
        super().__init__(NodeType.EFFECT, width, height, posX, posY, 0, 0, 0, imageString, -1)

        self.type = type

        self.entity = None
        self.heightOriginal = height
        self.timeLeft = self.EFFECT_TIME
        self.widthOriginal = width

        #Depending on the Effect type
        if self.type is EffectType.HEALTH_BAR:
            self.setColour(0, 255, 0)
            self.timeLeft = self.TIME_HEALTH_BAR
        elif self.type is EffectType.EXPLOSION:
            self.timeLeft = self.TIME_EXPLOSION
        elif self.type is EffectType.IMPLOSION:
            self.timeLeft = self.TIME_IMPLOSION

    #Define a Explosion Effect factory
    def Explosion(width, height, posX, posY):
        return Effect(width, height, posX, posY, Effect.IMAGE_EXPLOSION, EffectType.EXPLOSION)

    #Define a Implosion Effect factory
    def Implosion(width, height, posX, posY):
        return Effect(width, height, posX, posY, Effect.IMAGE_EXPLOSION, EffectType.IMPLOSION)

    #Define a Health Bar Effect factory
    def HealthBar(width, height, posX, posY):
        return Effect(width, height, posX, posY, Effect.IMAGE_HEALTH_BAR, EffectType.HEALTH_BAR)

    #Reset timeLeft
    def resetTimeLeft(self):
        #Depending on the Effect type
        if self.type is EffectType.HEALTH_BAR:
            self.timeLeft = self.TIME_HEALTH_BAR
        elif self.type is EffectType.EXPLOSION:
            self.timeLeft = self.TIME_EXPLOSION

    #Update the Effect status
    def update(self, frameDeltaTime):
        self.timeLeft -= frameDeltaTime

        #If the Effect has expired, return true
        if self.timeLeft < 0:
            return True

        #Depending on the Effect type
        if self.type is EffectType.HEALTH_BAR:
            pass
        elif self.type is EffectType.EXPLOSION:
            newWidth = int(self.widthOriginal * (1 + self.SIZE_MOD_EXPLOSION * (self.TIME_EXPLOSION - self.timeLeft) / self.TIME_EXPLOSION))
            newHeight = int(self.heightOriginal * (1 + self.SIZE_MOD_EXPLOSION * (self.TIME_EXPLOSION - self.timeLeft) / self.TIME_EXPLOSION))
            newTransparency = int(self.TRANSPARENCY_EXPLOSION * self.timeLeft / self.TIME_EXPLOSION)
            self.setSize(newWidth, newHeight)
            self.setTransparency(newTransparency)
        elif self.type is EffectType.IMPLOSION:
            newWidth = int(self.widthOriginal * (1 + self.SIZE_MOD_EXPLOSION * self.timeLeft / self.TIME_IMPLOSION))
            newHeight = int(self.heightOriginal * (1 + self.SIZE_MOD_EXPLOSION * self.timeLeft / self.TIME_IMPLOSION))
            newTransparency = int(self.TRANSPARENCY_EXPLOSION * self.timeLeft / self.TIME_IMPLOSION)

            self.setSize(newWidth, newHeight)
            self.setTransparency(newTransparency)

        return False



