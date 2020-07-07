#!/usr/bin/python

#Import libraries
from node import *

#Define an Enum for AttackType
class AttackType(Enum):
    MELEE = 1
    RANGED = 2
    SPELL = 3
    SUMMON = 4

#Define an Enum for EntityImage
class EntityImage(Enum):
    HUMAN = "./resources/entity_human.png"
    ROBOT = "./resources/entity_robot.png"

#Define an Enum for EntityState
class EntityState(Enum):
    NORMAL = 1
    DEAD = 2
    IMMORTAL = 3

#Define an Enum for EntityType
class EntityType(Enum):
    HUMAN = 1
    ROBOT = 2

#Define a class for Entitys
class Entity(Node):
    HEIGHT_DEFAULT = 48					#The default height for Entitys
    JUMP_HEIGHT_MOD = 2.5				#The jump height multiplier
    WIDTH_DEFAULT = 24					#The default width for Entitys

    #Define the constructor
    def __init__(self, width, height, posX, posY, rotation, dirX, dirY, imageString, team, name, type):
        super().__init__(NodeType.ENTITY, width, height, posX, posY, rotation, dirX, dirY, imageString, team, name)

        #Set Node fields
        self.type = type				#The Entity type

        #Set Entity fields
        self.attackRange = 20				#The Entitys current attackRange
        self.attackRangeSQ = 400			#The Entitys current attackRange squared
        self.attackStyle = AttackType.MELEE		#The Entitys current attackStyle
        self.attackType = AttackType.MELEE		#The Entitys current attackType
        self.healthCurrent = 10				#The Entitys current health
        self.healthMax = 10				#The Entitys max health
        self.healthRegen = 1				#The Entitys health regen
        self.manaCurrent = 10				#The Entitys current mana
        self.manaMax = 10				#The Entitys max mana
        self.manaRegen = 1				#The Entitys mana regen
        self.meleeDamage = 1				#The Entitys melee damage
        self.meleeRange = 20				#The Entitys melee range
        self.meleeRateOfFire = 1			#The Entitys melee rate of fire
        self.meleeTimeLeft = -1				#The Entitys melee timeLeft
        self.rangedAmmo = 10				#The Entitys Ranged Ammo
        self.rangedAmmoCost = 1				#The Entitys Ranged Ammo cost
        self.rangedDamage = 1				#The Entitys Ranged damage
        self.rangedRange = 200				#The Entitys Ranged range
        self.rangedRateOfFire = 1			#The Entitys Ranged rate of fire
        self.rangedSpeed = 200				#The Entitys Ranged speed
        self.rangedTimeLeft = -1			#The Entitys Ranged timeLeft
        self.speed = 25					#The Entitys speed
        self.spellDamage = 1				#The Entitys Spell damage
        self.spellManaCost = 1				#The Entitys Spell mana cost
        self.spellRange = 200				#The Entitys Spell range
        self.spellRateOfFire = 1			#The Entitys Spell rate of fire
        self.spellSpeed = 300				#The Entitys Spell speed
        self.spellTimeLeft = -1				#The Entitys Spell timeLeft
        self.state = EntityState.NORMAL			#The Entitys state

        #Set Entity pointers
        self.healthBar = None				#The Entitys healthBar
        self.target = None				#The Entitys target

    #Define a Entity factory
    def Entity(posX, posY, rotation, dirX, dirY, team, type):
        imageString = ""
        name = ""

        #Depending on the type, set the imageString
        if type is EntityType.HUMAN:
            imageString = EntityImage.HUMAN.value
            name = "Human"
        elif type is EntityType.ROBOT:
            imageString = EntityImage.ROBOT.value
            name = "Robot"

        return Entity(Entity.WIDTH_DEFAULT, Entity.HEIGHT_DEFAULT, posX, posY, rotation, dirX, dirY, imageString, team, name, type)

    #Have the Entity attack using Melee, returning True if successful
    def attackMelee(self):
        #If can attack using Melee, set meleeTimeLeft
        if self.meleeTimeLeft < 0:
            self.meleeTimeLeft = self.meleeRateOfFire

            return True

        return False

    #Have the Entity attack using Ranged, returning True if successful
    def attackRanged(self):
        #If can attack using Ranged, set rangedTimeLeft and remove Ranged Ammo
        if self.rangedTimeLeft < 0 and self.hasRangedAmmo():
            self.rangedTimeLeft = self.rangedRateOfFire
            self.rangedAmmo -= self.rangedAmmoCost

            return True

        return False

    #Have the Entity attack using Spell, returning True if successful
    def attackSpell(self):
        #If can attack using Spell, set spellTimeLeft and remove Spell mana cost
        if self.spellTimeLeft < 0 and self.hasSpellMana():
            self.spellTimeLeft = self.spellRateOfFire
            self.manaCurrent -= self.spellManaCost

            return True

        return False

    #Get whether the Entity can attack with the current attackType
    def canAttack(self):
        #Depending on the attackType and whether the Entity can attack, return True
        if self.attackType is AttackType.MELEE and self.meleeTimeLeft < 0:
            return True
        elif self.attackType is AttackType.RANGED and self.rangedTimeLeft < 0 and self.hasRangedAmmo():
            return True
        elif self.attackType is AttackType.SPELL and self.spellTimeLeft < 0 and self.hasSpellMana():
            return True
        elif self.attackType is AttackType.SUMMON and self.spellTimeLeft < 0 and self.hasSpellMana():
            return True

        return False

    #Damage the Entity and update its state if it dies
    def damage(self, damage):
        if self.state is EntityState.NORMAL:
            self.healthCurrent -= damage
            if self.healthCurrent < 0:
                self.state = EntityState.DEAD

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
        #TODO implement changing of attackStyle
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

        #Depending on the attackType, set attackRange
        if self.attackType == AttackType.MELEE:
            self.attackRange = self.meleeRange
            self.attackRangeSQ = self.meleeRange * self.meleeRange
        elif self.attackType == AttackType.RANGED:
            self.attackRange = self.rangedRange
            self.attackRangeSQ = self.rangedRange * self.rangedRange
        elif self.attackType == AttackType.SPELL:
            self.attackRange = self.spellRange
            self.attackRangeSQ = self.spellRange * self.spellRange
        elif self.attackType == AttackType.SUMMON:
            self.attackRange = self.spellRange
            self.attackRangeSQ = self.spellRange * self.spellRange

    #Update the Entity status
    def update(self, frameDeltaTime):
        self.meleeTimeLeft -= frameDeltaTime
        self.rangedTimeLeft -= frameDeltaTime
        self.spellTimeLeft -= frameDeltaTime

        #If the Entity is dead, return True
        if self.state is EntityState.DEAD:
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



