#!/usr/bin/python

#Import libraries
from node import *

#Define an Enum for TerrainImage
class TerrainImage(Enum):
    WATER = "./resources/terrain_water.png"
    SAND = "./resources/terrain_sand.png"
    DIRT = "./resources/terrain_dirt.png"
    COPPER = "./resources/terrain_copper.png"
    TIN = "./resources/terrain_tin.png"
    IRON = "./resources/terrain_iron.png"
    COAL = "./resources/terrain_coal.png"
    SILVER = "./resources/terrain_silver.png"
    GOLD = "./resources/terrain_gold.png"
    PLATINUM = "./resources/terrain_platinum.png"

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

#Define a class for Terrain
class Terrain(Node):
    TERRAIN_SIZE = 32					#The size of Terrain
    TERRAIN_SIZE_HALF = 16				#The size of Terrain halved

    #Define the constructor
    def __init__(self, posX, posY, imageString, name, type):
        super().__init__(NodeType.TERRAIN, self.TERRAIN_SIZE, self.TERRAIN_SIZE, posX, posY, 0, 0, 0, imageString, None, name)

        #Set Node fields
        self.type = type				#The Terrain type

    #Define a Terrain factory
    def Terrain(posX, posY, type):
        imageString = ""
        name = ""

        #Depending on the type, set the imageString
        if type is TerrainType.WATER:
            imageString = TerrainImage.WATER.value
            name = "Water"
        elif type is TerrainType.SAND:
            imageString = TerrainImage.SAND.value
            name = "Sand"
        elif type is TerrainType.DIRT:
            imageString = TerrainImage.DIRT.value
            name = "Dirt"
        elif type is TerrainType.COPPER:
            imageString = TerrainImage.COPPER.value
            name = "Copper"
        elif type is TerrainType.TIN:
            imageString = TerrainImage.TIN.value
            name = "Tin"
        elif type is TerrainType.IRON:
            imageString = TerrainImage.IRON.value
            name = "Iron"
        elif type is TerrainType.COAL:
            imageString = TerrainImage.COAL.value
            name = "Coal"
        elif type is TerrainType.SILVER:
            imageString = TerrainImage.SILVER.value
            name = "Silver"
        elif type is TerrainType.GOLD:
            imageString = TerrainImage.GOLD.value
            name = "Gold"
        elif type is TerrainType.PLATINUM:
            imageString = TerrainImage.PLATINUM.value
            name = "Platinum"

        return Terrain(posX, posY, imageString, name, type)



