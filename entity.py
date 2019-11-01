#!/usr/bin/python

#Import libraries
from node import *

#Define an Enum for EntityState
class EntityState(Enum):    #TODO not used
    MOVING = 1
    JUMPING = 2
    SWIMMING = 3
    DEAD = 4
    IMMORTAL = 5

#Define a class for Entitys
class Entity(Node):
    HEIGHT_DEFAULT = 48
    JUMP_HEIGHT_MOD = 2.5
    WIDTH_DEFAULT = 24
    #Define the constructor
    def __init__(self, width, height, posX, posY, rotation, dirX, dirY, imageString, team):
        super().__init__(NodeType.ENTITY, width, height, posX, posY, rotation, dirX, dirY, imageString)

        self.state = EntityState.JUMPING
        self.team = team

    #Get the Entitys jump height
    def getJumpHeight(self):
        return self.height * self.JUMP_HEIGHT_MOD

    #Have the Entity jump
    def jump(self):
        self.direction.y -= self.height * self.JUMP_HEIGHT_MOD



