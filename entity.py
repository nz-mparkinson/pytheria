#!/usr/bin/python

#Import libraries
from node import *

#Define an Enum for EntityType
class EntityType(Enum):
    NORMAL = 1
    DEAD = 2
    IMMORTAL = 3

#Define a class for Entitys
class Entity(Node):
    HEIGHT_DEFAULT = 48
    JUMP_HEIGHT_MOD = 2.5
    WIDTH_DEFAULT = 24
    #Define the constructor
    def __init__(self, width, height, posX, posY, rotation, dirX, dirY, imageString, team):
        super().__init__(NodeType.ENTITY, width, height, posX, posY, rotation, dirX, dirY, imageString)

        self.team = team
        self.type = EntityType.NORMAL

        self.attackDamage = 1
        self.attackRange = 20
        self.attackRateOfFire = 1
        self.healthCurrent = 10
        self.healthMax = 10
        self.healthRegen = 1
        self.manaCurrent = 10
        self.manaMax = 10
        self.manaRegen = 1
        self.rangedDamage = 1
        self.rangedRange = 50
        self.rangedRateOfFire = 1
        self.rangedSpeed = 50
        self.speed = 25
        self.spellDamage = 1
        self.spellRange = 100
        self.spellRateOfFire = 1
        self.spellSpeed = 100

    #Damage the Entity, return true if the Entity dies
    def damage(self, damage):
        if self.type is EntityType.NORMAL:
            self.healthCurrent -= damage

        if self.healthCurrent <= 0:
            return True

        return False

    #Get the Entitys jump height
    def getJumpHeight(self):
        return self.height * self.JUMP_HEIGHT_MOD

    #Have the Entity jump
    def jump(self):
        self.direction.y -= self.height * self.JUMP_HEIGHT_MOD

    #Update the Entity status
    def update(self, frameDeltaTime):
        #Regen health
        self.healthCurrent += self.healthRegen * frameDeltaTime
        if self.healthCurrent > self.healthMax:
            self.healthCurrent = self.healthMax

        #Regen mana
        self.manaCurrent += self.manaRegen * frameDeltaTime
        if self.manaCurrent > self.manaMax:
            self.manaCurrent = self.manaMax

    

