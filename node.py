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
    EFFECT = 4

#Define an Enum for Team
class Team(Enum):
    FRIEND = 1
    ENEMY = 2

#Define a class for Nodes, visible objects within the game
class Node:
    #Define the constructor
    def __init__(self, nodeType, width, height, posX, posY, rotation, dirX, dirY, imageString, team, name):

        #Set the Node fields
        self.nodeType = nodeType			#The Node type
        self.width = width				#The Nodes width
        self.widthHalf = width // 2			#The Nodes width halved
        self.height = height				#The Nodes height
        self.heightHalf = height // 2			#The Nodes height halved
        self.position = Vector2f(posX, posY)		#The Nodes position, note: the y-axis is inverted, -1 is up
        self.rotation = rotation			#The Nodes rotation
        self.direction = Vector2f(dirX, dirY)		#The Nodes direction
        self.team = team				#The Nodes team
        self.name = name				#The Nodes name

        #Initialize Node fields
        self.image = None				#The Nodes image
        self.imageFlip = False				#Whether the images has been flipped horizontally
        self.imageOriginal = None			#The Nodes image original
        self.movement = Vector2f(0, 0)			#The Nodes last movement direction

        #Load the image, note: keeping a copy of the original as rotating the image looses quality
        self.imageOriginal = pygame.image.load(imageString).convert_alpha()
        self.image = self.imageOriginal

        #Set the Node rotation/size
        self.setRotation(rotation)

    #Define a Node factory
    def Node(width, height, posX, posY, imageString):
        return Node(NodeType.EFFECT, width, height, posX, posY, 0, 0, 0, imageString, None, "Node")

    #Accelerate the Node in a direction
    def accelerate(self, x, y):
        self.direction.x += x
        self.direction.y += y

    #Deccelerate the Node
    def deccelerate(self, speedToRemove):
        self.direction.removeMagnitude(speedToRemove)

    #Ensure the Node isn't going faster then maxSpeed
    def ensureMaxSpeed(self, maxSpeed):
        if self.direction.getLengthSQ() > maxSpeed * maxSpeed:
            self.direction.setLength(maxSpeed)

    #Flip the Node image horizontally
    def flipImage(self):
        self.image = pygame.transform.flip(self.image, 1, 0)

        #Toggle imageFlip
        if self.imageFlip:
            self.imageFlip = False
        else:
            self.imageFlip = True

    #Get center positon
    def getCenter(self):
        return Vector2f(self.position.x + self.widthHalf, self.position.y + self.heightHalf)

    #Get center positon x
    def getCenterX(self):
        return self.position.x + self.widthHalf

    #Get center positon
    def getCenterY(self):
        return self.position.y + self.heightHalf

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

        #Set the Node movement
        self.movement.x = x
        self.movement.y = y

        #If the image is facing the wrong way compared to the Node movement, flip the image
        if self.movement.x < 0 and self.imageFlip:
            self.flipImage()
        if self.movement.x > 0 and not self.imageFlip:
            self.flipImage()

    #Rotate the Node
    def rotate(self, rotationDelta):
        self.setRotation(self.rotation + rotationDelta)

    #Set the Node colour
    def setColour(self, red, green, blue):
        arr = pygame.surfarray.pixels3d(self.image)
        arr[:,:,0] = red
        arr[:,:,1] = green
        arr[:,:,2] = blue
        arr = pygame.surfarray.pixels3d(self.imageOriginal)
        arr[:,:,0] = red
        arr[:,:,1] = green
        arr[:,:,2] = blue

    #Set the Node height
    def setHeight(self, height):
        self.height = height
        self.heightHalf = height // 2
        self.image = pygame.transform.scale(self.imageOriginal, (self.width, height))

    #set the Node image
    def setImage(self, imageString):
        #Load the image, note: keeping a copy of the original as rotating the image looses quality
        self.imageOriginal = pygame.image.load(imageString).convert_alpha()
        self.image = self.imageOriginal
        self.imageFlip = False

        #Set the Node rotation/size
        self.setRotation(self.rotation)

    #Set the Node rotation, note: requires that Node size is also set
    def setRotation(self, rotation):
        self.rotation = rotation
        self.image = pygame.transform.rotozoom(self.imageOriginal, rotation, 1)
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.imageFlip = False

    #Set the Node size
    def setSize(self, width, height):
        self.position.x -= (width - self.width) / 2
        self.position.y -= (height - self.height) / 2
        self.width = width
        self.widthHalf = width // 2
        self.height = height
        self.heightHalf = height // 2
        self.image = pygame.transform.scale(self.imageOriginal, (width, height))
        self.imageFlip = False

    #Set the Node transparency
    def setTransparency(self, alpha):
        temp = pygame.Surface((self.image.get_width(), self.image.get_height())).convert()
        temp.blit(self.image, (0, 0))
        temp.set_alpha(alpha)
        temp.set_colorkey((0, 0, 0))
        self.image = temp

    #Set the Node width
    def setWidth(self, width):
        self.width = width
        self.widthHalf = width // 2
        self.image = pygame.transform.scale(self.imageOriginal, (width, self.height))

    #Update the Node status
    def update(self, frameDeltaTime):
        pass



