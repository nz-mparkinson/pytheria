#!/usr/bin/python

#Import libraries
from node import *

#Define a class for Ammo
class Ammo(Node):
    AMMO_SIZE = 16

    #Define the constructor
    def __init__(self, width, height, top, left, rotation, dirX, dirY, imageString):
        super().__init__(NodeType.AMMO, self.AMMO_SIZE, self.AMMO_SIZE, top, left, rotation, dirX, dirY, imageString) 



