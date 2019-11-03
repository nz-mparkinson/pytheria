#!/usr/bin/python

#Import libraries
from node import *

#Define an Enum for AttackType
class AttackType(Enum):
    MELEE = 1
    RANGED = 2
    SPELL = 3
    SUMMON = 4

#Define an Enum for EntityType
class EntityType(Enum):
    NORMAL = 1
    DEAD = 2
    IMMORTAL = 3

#Define an Enum for EntityImage
class EntityImage(Enum):
    NORMAL = "../resources/mine2/entity_normal.png"
    DEAD = "../resources/mine2/entity_dead.png"
    IMMORTAL = "../resources/mine2/entity_immortal.png"

#Define a class for Entitys
class Entity(Node):
    HEIGHT_DEFAULT = 48
    JUMP_HEIGHT_MOD = 2.5
    WIDTH_DEFAULT = 24

    #Define the constructor
    def __init__(self, width, height, posX, posY, rotation, dirX, dirY, imageString, type, team):
        super().__init__(NodeType.ENTITY, width, height, posX, posY, rotation, dirX, dirY, imageString, team)

        #Set Node fields
        self.type = type

        #Set Entity fields
        self.attackDamage = 1
        self.attackRange = 20
        self.attackRateOfFire = 1
        self.attackStyle = AttackType.MELEE
        self.attackTimeLeft = -1
        self.attackType = AttackType.MELEE
        self.healthCurrent = 10
        self.healthMax = 10
        self.healthRegen = 1
        self.manaCurrent = 10
        self.manaMax = 10
        self.manaRegen = 1
        self.rangedAmmo = 10
        self.rangedAmmoCost = 1
        self.rangedDamage = 1
        self.rangedRange = 200
        self.rangedRateOfFire = 1
        self.rangedSpeed = 200
        self.rangedTimeLeft = -1
        self.speed = 25
        self.spellDamage = 1
        self.spellManaCost = 1
        self.spellRange = 200
        self.spellRateOfFire = 1
        self.spellSpeed = 300
        self.spellTimeLeft = -1

        #Set Entity pointers
        self.healthBar = None

    #Define a Entity factory
    def Entity(width, height, posX, posY, rotation, dirX, dirY, type, team):
        imageString = ""

        #Depending on the type, set the imageString
        if type is EntityType.NORMAL:
            imageString = EntityImage.NORMAL.value
        elif type is EntityType.DEAD:
            imageString = EntityImage.DEAD.value
        elif type is EntityType.IMMORTAL:
            imageString = EntityImage.IMMORTAL.value

        return Entity(width, height, posX, posY, rotation, dirX, dirY, imageString, type, team)

    #Have the Entity attack using Melee, returning True if successful
    def attackMelee(self):
        if self.attackTimeLeft < 0:
            #Set attackTimeLeft
            self.attackTimeLeft += self.attackRateOfFire

            return True

        return False

    #Have the Entity attack using Ranged, returning True if successful
    def attackRanged(self):
        if self.rangedTimeLeft < 0 and self.hasRangedAmmo():
            #Set rangedTimeLeft
            self.rangedTimeLeft += self.rangedRateOfFire
            #Rmove ranged Ammo
            self.rangedAmmo -= self.rangedAmmoCost

            return True

        return False

    #Have the Entity attack using Spell, returning True if successful
    def attackSpell(self):
        if self.spellTimeLeft < 0 and self.hasSpellMana():
            #Set spellTimeLeft
            self.spellTimeLeft += self.spellRateOfFire
            #Remove Spell mana cost
            self.manaCurrent -= self.spellManaCost

            return True

        return False

    #Damage the Entity, return true if the Entity dies
    def damage(self, damage):
        if self.type is EntityType.NORMAL:
            self.healthCurrent -= damage

    #Get the Entitys jump height
    def getJumpHeight(self):
        return self.height * self.JUMP_HEIGHT_MOD

    #Get the Entitys health percentage
    def getHealthPercentage(self):
        if self.healthCurrent <= 0:
            return 0

        return self.healthCurrent / self.healthMax

    #Get the Entitys mana percentage
    def getManaPercentage(self):
        if self.manaCurrent <= 0:
            return 0

        return self.manaCurrent / self.manaMax

    #Get whether the Entity has ranged Ammo
    def hasRangedAmmo(self):
        if self.rangedAmmo >= self.rangedAmmoCost:
            return True

        return False

    #Get whether the Entity has spell mana
    def hasSpellMana(self):
        if self.manaCurrent >= self.spellManaCost:
            return True

        return False

    #Have the Entity jump
    def jump(self):
        self.direction.y -= self.height * self.JUMP_HEIGHT_MOD

    #Toggle the Entity AttackStyle forwards or backwards
    def toggleAttackStyle(self, forward):
        if forward:
            if self.attackStyle == AttackType.SUMMON:
                self.attackStyle = AttackType.MELEE
            else:
                self.attackStyle = AttackType(self.attackStyle.value + 1)
        else:
            if self.attackStyle == AttackType.MELEE:
                self.attackStyle = AttackType.SUMMON
            else:
                self.attackStyle = AttackType(self.attackStyle.value - 1)

    #Toggle the Entity AttackType forwards or backwards
    def toggleAttackType(self, forward):
        if forward:
            if self.attackType == AttackType.SUMMON:
                self.attackType = AttackType.MELEE
            else:
                self.attackType = AttackType(self.attackType.value + 1)
        else:
            if self.attackType == AttackType.MELEE:
                self.attackType = AttackType.SUMMON
            else:
                self.attackType = AttackType(self.attackType.value - 1)

    #Update the Entity status
    def update(self, frameDeltaTime):
        self.attackTimeLeft -= frameDeltaTime
        self.rangedTimeLeft -= frameDeltaTime
        self.spellTimeLeft -= frameDeltaTime

        #If the Entity is dead, return True
        if self.healthCurrent <= 0:
            return True

        #Regen health
        self.healthCurrent += self.healthRegen * frameDeltaTime
        if self.healthCurrent > self.healthMax:
            self.healthCurrent = self.healthMax

        #Regen mana
        self.manaCurrent += self.manaRegen * frameDeltaTime
        if self.manaCurrent > self.manaMax:
            self.manaCurrent = self.manaMax

        return False



