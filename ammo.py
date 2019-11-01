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
    def __init__(self, posX, posY, dirX, dirY, imageString, type, team, speed):
        super().__init__(NodeType.AMMO, self.AMMO_SIZE, self.AMMO_SIZE, posX, posY, Vector2f(dirX, dirY).getAngle(), dirX, dirY, imageString)

        self.team = team
        self.type = type

        #Set the Ammo speed
        self.direction.setLength(speed)



