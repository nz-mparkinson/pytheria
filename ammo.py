#!/usr/bin/python

#Import libraries
from node import *

#Define an Enum for AmmoImage
class AmmoImage(Enum):
    RANGED = "./resources/circle_128.png"
    SPELL = "./resources/circle_128.png"

#Define an Enum for AmmoType
class AmmoType(Enum):
    RANGED = 1
    SPELL = 2

#Define a class for Ammo
class Ammo(Node):
    AMMO_SIZE = 16
    AMMO_SIZE_HALF = 8

    #Define the constructor
    def __init__(self, posX, posY, dirX, dirY, imageString, team, type, damage, range, speed):
        super().__init__(NodeType.AMMO, self.AMMO_SIZE, self.AMMO_SIZE, posX, posY, Vector2f(dirX, dirY).getAngle(), dirX, dirY, imageString, team, "Ammo")

        #Set Node fields
        self.type = type

        #Set Ammo fields
        self.damage = damage

        #Set the Ammo speed
        self.direction.setLength(speed)

        #Derive how long the Ammo lasts
        self.timeLeft = range / speed

    #Define a Ammo factory
    def Ammo(posX, posY, dirX, dirY, team, type, damage, range, speed):
        imageString = ""

        #Depending on the type, set the imageString
        if type is AmmoType.RANGED:
            imageString = AmmoImage.RANGED.value
        elif type is AmmoType.SPELL:
            imageString = AmmoImage.SPELL.value

        return Ammo(posX, posY, dirX, dirY, imageString, team, type, damage, range, speed)

    #Update the Ammo status
    def update(self, frameDeltaTime):
        self.timeLeft -= frameDeltaTime

        #If the Ammo has expired, return true
        if self.timeLeft < 0:
            return True

        return False



