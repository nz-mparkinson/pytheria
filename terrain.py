#!/usr/bin/python

#Import libraries
from node import *

#Define a class for Terrain
class Terrain(Node):
    TERRAIN_SIZE = 32

    #Define the constructor
    def __init__(self, posX, posY, imageString):
        super().__init__(NodeType.TERRAIN, self.TERRAIN_SIZE, self.TERRAIN_SIZE, posX, posY, 0, 0, 0, imageString) 



