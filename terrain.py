#!/usr/bin/python

#Import libraries
from node import *

#Define an Enum for TerrainType
class TerrainType(Enum):
    WATER = 1
    SAND = 2
    DIRT = 3
    COPPER = 4
    TIN = 5
    IRON = 6
    COAL = 7
    SILVER = 8
    GOLD = 9
    PLATINUM = 10

#Define an Enum for TerrainImage
class TerrainImage(Enum):
    WATER = "../resources/mine2/test.png"
    SAND = "../resources/mine2/test.png"
    DIRT = "../resources/mine2/test.png"
    COPPER = "../resources/mine2/test.png"
    TIN = "../resources/mine2/test.png"
    IRON = "../resources/mine2/test.png"
    COAL = "../resources/mine2/test.png"
    SILVER = "../resources/mine2/test.png"
    GOLD = "../resources/mine2/test.png"
    PLATINUM = "../resources/mine2/test.png"

#Define a class for Terrain
class Terrain(Node):
    TERRAIN_SIZE = 32
    TERRAIN_SIZE_HALF = 16

    #Define the constructor
    def __init__(self, posX, posY, imageString, type):
        super().__init__(NodeType.TERRAIN, self.TERRAIN_SIZE, self.TERRAIN_SIZE, posX, posY, 0, 0, 0, imageString, -1)

        #Set Node fields
        self.type = type

    #Define a Terrain factory
    def Terrain(posX, posY, type):
        imageString = ""

        #Depending on the type, set the imageString
        if type is TerrainType.WATER:
            imageString = TerrainImage.WATER.value
        elif type is TerrainType.SAND:
            imageString = TerrainImage.SAND.value
        elif type is TerrainType.DIRT:
            imageString = TerrainImage.DIRT.value
        elif type is TerrainType.COPPER:
            imageString = TerrainImage.COPPER.value
        elif type is TerrainType.TIN:
            imageString = TerrainImage.TIN.value
        elif type is TerrainType.IRON:
            imageString = TerrainImage.IRON.value
        elif type is TerrainType.COAL:
            imageString = TerrainImage.COAL.value
        elif type is TerrainType.SILVER:
            imageString = TerrainImage.SILVER.value
        elif type is TerrainType.GOLD:
            imageString = TerrainImage.GOLD.value
        elif type is TerrainType.PLATINUM:
            imageString = TerrainImage.PLATINUM.value

        return Terrain(posX, posY, imageString, type)



