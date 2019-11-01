#!/usr/bin/python

#Import libraries
from enum import Enum
import pygame
from pygame.locals import *

from vector2f import *

#Define an Enum for NodeType
class NodeType(Enum):
    TERRAIN = 1
    ENTITY = 2
    AMMO = 3

#Define a class for Nodes, objects within the game
class Node:
    #Define the constructor
    def __init__(self, nodeType, width, height, posX, posY, rotation, dirX, dirY, imageString):
        #Load the image, note: keeping a copy of the original as rotating the image looses quality
        self.imageOriginal = pygame.image.load(imageString)
        self.image = self.imageOriginal

        self.nodeType = nodeType
        self.width = width
        self.height = height
        self.position = Vector2f(posX, posY)
        self.rotation = rotation
        self.direction = Vector2f(dirX, dirY)

        #Set the Node rotation/size
        self.setRotation(rotation)

    #Accelerate the Node in a direction
    def accelerate(self, x, y):
        self.direction.x += x
        self.direction.y += y

    #Deccelerate the Node
    def deccelerate(self, speedToRemove):
        self.direction.removeMagnitude(speedToRemove)

    #Get whether a Node is inside another Node
    def isInside(self, other):
        if self.position.x + self.width < other.position.x:
            return False
        elif self.position.y + self.height < other.position.y:
            return False
        elif other.position.x + other.width < self.position.x:
            return False
        elif other.position.y + other.height < self.position.y:
            return False

        return True

    #Move the Node in a direction
    def move(self, x, y):
        self.position.x += x
        self.position.y += y

    #Rotate the Node
    def rotate(self, rotationDelta):
        self.setRotation(self.rotation + rotationDelta)

    #Set the Node rotation, note: requires that Node size is also set
    def setRotation(self, rotation):
        self.rotation = rotation
        self.image = pygame.transform.rotozoom(self.imageOriginal, rotation, 1)
        self.setSize(self.width, self.height)

    #Set the Node size
    def setSize(self, width, height):
        self.width = width
        self.height = height
        self.image = pygame.transform.scale(self.image, (width, height))

    #Update the Node
    def update(self, frameDeltaTime):
        pass



