#!/usr/bin/python

#Import libraries
from node import *

#Define an Enum for EntityState
class EntityState(Enum):
    MOVING = 1
    JUMPING = 2
    SWIMMING = 3
    DEAD = 4
    IMMORTAL = 5

#Define a class for Entitys
class Entity(Node):
    #Define the constructor
    def __init__(self, width, height, top, left, rotation, dirX, dirY, imageString):
        super().__init__(NodeType.ENTITY, width, height, top, left, rotation, dirX, dirY, imageString) 

        self.state = EntityState.JUMPING



