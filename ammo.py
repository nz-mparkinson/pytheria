#!/usr/bin/python

#Import libraries
from node import *

#Define an Enum for AmmoType
class AmmoType(Enum):
    RANGED = 1
    SPELL = 2

#Define a class for Ammo
class Ammo(Node):
    AMMO_SIZE = 16

    #Define the constructor
    def __init__(self, posX, posY, dirX, dirY, imageString, team, type, damage, range, speed):
        super().__init__(NodeType.AMMO, self.AMMO_SIZE, self.AMMO_SIZE, posX, posY, Vector2f(dirX, dirY).getAngle(), dirX, dirY, imageString, team)

        self.type = type
        self.damage = damage

        #Set the Ammo speed
        self.direction.setLength(speed)

        #Derive how long the Ammo lasts
        self.timeLeft = range / speed

    #Update the Ammo status
    def update(self, frameDeltaTime):
        self.timeLeft -= frameDeltaTime

        if self.timeLeft < 0:
            return True

        return False



