#!/usr/bin/python

#Import libraries
from node import *

#Define an Enum for EffectType
class EffectType(Enum):
    HEALTH_BAR = 1
    EXPLOSION = 2
    IMPLOSION = 3
    EXPLOSION_VERTICAL = 4
    RETICLE = 5

#Define a class for Effect
class Effect(Node):
    COLOUR_HEALTH_BAR = (0, 255, 0)
    COLOUR_RETICLE = (170, 170, 170)
    IMAGE_EXPLOSION = "../resources/mine/circle.png"
    IMAGE_EXPLOSION_VERTICAL = "../resources/mine/square.png"
    IMAGE_HEALTH_BAR = "../resources/mine/healthbar.png"
    IMAGE_IMPLOSION = "../resources/mine/circle.png"
    IMAGE_RETICLE = "../resources/mine/box.png"
    SIZE_MOD_EXPLOSION = 5
    SIZE_MOD_EXPLOSION_VERTICAL = 5
    SIZE_MOD_IMPLOSION = 5
    TIME_EXPLOSION = 0.2
    TIME_EXPLOSION_VERTICAL = 0.5
    TIME_HEALTH_BAR = 3
    TIME_IMPLOSION = 0.5
    TRANSPARENCY_EXPLOSION = 150
    TRANSPARENCY_EXPLOSION_VERTICAL = 150
    TRANSPARENCY_IMPLOSION = 150

    #Define the constructor
    def __init__(self, width, height, posX, posY, imageString, type):
        super().__init__(NodeType.EFFECT, width, height, posX, posY, 0, 0, 0, imageString, -1)

        #Set Node fields
        self.type = type

        #Set Effect fields
        self.entity = None
        self.heightOriginal = height
        self.widthOriginal = width

        #Depending on the Effect type, set timeLeft etc.
        if self.type is EffectType.HEALTH_BAR:
            self.timeLeft = self.TIME_HEALTH_BAR
            self.setColour(self.COLOUR_HEALTH_BAR[0], self.COLOUR_HEALTH_BAR[1], self.COLOUR_HEALTH_BAR[2])
        elif self.type is EffectType.EXPLOSION:
            self.timeLeft = self.TIME_EXPLOSION
        elif self.type is EffectType.IMPLOSION:
            self.timeLeft = self.TIME_IMPLOSION
        elif self.type is EffectType.EXPLOSION_VERTICAL:
            self.timeLeft = self.TIME_EXPLOSION_VERTICAL
        elif self.type is EffectType.RETICLE:
            self.timeLeft = -1
            self.setColour(self.COLOUR_RETICLE[0], self.COLOUR_RETICLE[1], self.COLOUR_RETICLE[2])

    #Define a Explosion Effect factory
    def Explosion(width, height, posX, posY):
        return Effect(width, height, posX, posY, Effect.IMAGE_EXPLOSION, EffectType.EXPLOSION)

    #Define a Explosion Vertical Effect factory
    def ExplosionVertical(width, height, posX, posY):
        return Effect(width, height, posX, posY, Effect.IMAGE_EXPLOSION_VERTICAL, EffectType.EXPLOSION_VERTICAL)

    #Define a Implosion Effect factory
    def Implosion(width, height, posX, posY):
        return Effect(width, height, posX, posY, Effect.IMAGE_IMPLOSION, EffectType.IMPLOSION)

    #Define a Health Bar Effect factory
    def HealthBar(width, height, posX, posY):
        return Effect(width, height, posX, posY, Effect.IMAGE_HEALTH_BAR, EffectType.HEALTH_BAR)

    #Define a Reticle Effect factory
    def Reticle(width, height, posX, posY):
        return Effect(width, height, posX, posY, Effect.IMAGE_RETICLE, EffectType.RETICLE)

    #Reset timeLeft depending on the Effect type
    def resetTimeLeft(self):
        if self.type is EffectType.HEALTH_BAR:
            self.timeLeft = self.TIME_HEALTH_BAR

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
            #Calculate new size/transparency
            newWidth = int(self.widthOriginal * (1 + self.SIZE_MOD_EXPLOSION * (self.TIME_EXPLOSION - self.timeLeft) / self.TIME_EXPLOSION))
            newHeight = int(self.heightOriginal * (1 + self.SIZE_MOD_EXPLOSION * (self.TIME_EXPLOSION - self.timeLeft) / self.TIME_EXPLOSION))
            newTransparency = int(self.TRANSPARENCY_EXPLOSION * self.timeLeft / self.TIME_EXPLOSION)

            #Set new size/transparency
            self.setSize(newWidth, newHeight)
            self.setTransparency(newTransparency)
        elif self.type is EffectType.IMPLOSION:
            #Calculate new size/transparency
            newWidth = int(self.widthOriginal * (1 + self.SIZE_MOD_IMPLOSION * self.timeLeft / self.TIME_IMPLOSION))
            newHeight = int(self.heightOriginal * (1 + self.SIZE_MOD_IMPLOSION * self.timeLeft / self.TIME_IMPLOSION))
            newTransparency = int(self.TRANSPARENCY_IMPLOSION * self.timeLeft / self.TIME_IMPLOSION)

            #Set new size/transparency
            self.setSize(newWidth, newHeight)
            self.setTransparency(newTransparency)
        elif self.type is EffectType.EXPLOSION_VERTICAL:
            #Calculate new size/transparency
            newHeight = int(self.heightOriginal * (1 + self.SIZE_MOD_EXPLOSION_VERTICAL * (self.TIME_EXPLOSION_VERTICAL - self.timeLeft) / self.TIME_EXPLOSION_VERTICAL))
            newTransparency = int(self.TRANSPARENCY_EXPLOSION_VERTICAL * self.timeLeft / self.TIME_EXPLOSION_VERTICAL)

            #Set new size/transparency
            self.setSize(self.width, newHeight)
            self.setTransparency(newTransparency)

        return False



