#!/usr/bin/python

#Import libraries
from node import *

#Define an Enum for EffectType
class EffectType(Enum):
    HEALTH_BAR = 1

#Define a class for Effect
class Effect(Node):
    EFFECT_TIME = 1

    #Define the constructor
    def __init__(self, width, height, posX, posY, imageString, type):
        super().__init__(NodeType.EFFECT, width, height, posX, posY, 0, 0, 0, imageString, -1)

        self.type = type

        self.timeLeft = self.EFFECT_TIME

    #Update the Effect status
    def update(self, frameDeltaTime):
        self.timeLeft -= frameDeltaTime

        if self.timeLeft < 0:
            return True

        return False



