#!/usr/bin/python

#Import libraries
from node import *

#Define an Enum for EffectType
class EffectType(Enum):
    EXPLOSION = 1
    EXPLOSION_VERTICAL = 2
    HEALTH_BAR = 3
    IMPLOSION = 4
    MANA_BAR = 5
    MELEE = 6
    RETICLE = 7

#Define a class for Effect
class Effect(Node):
    COLOUR_HEALTH_BAR = (0, 255, 0)			#The colour of the Health Bar Effect
    COLOUR_MANA_BAR = (0, 0, 255)			#The colour of the Mana Bar Effect
    COLOUR_RETICLE = (204, 204, 204)			#The colour of the Reticle Effect
    IMAGE_EXPLOSION = "./resources/circle_128.png"	#The image for the Explosion Effect
    IMAGE_EXPLOSION_VERTICAL = "./resources/square.png"	#The image for the Explosion Vertical Effect
    IMAGE_HEALTH_BAR = "./resources/square.png"		#The image for the Health Bar Effect
    IMAGE_IMPLOSION = "./resources/circle_128.png"	#The image for the Implosion Effect
    IMAGE_MANA_BAR = "./resources/square.png"		#The image for the Mana Bar Effect
    IMAGE_MELEE = "./resources/square.png"		#The image for the Melee Effect
    IMAGE_RETICLE = "./resources/box.png"		#The image for the Reticle Effect
    SIZE_MOD_EXPLOSION = 5				#The size multiplier the Explosion Effect grows to
    SIZE_MOD_EXPLOSION_VERTICAL = 5			#The size multiplier the Explosion Vertical Effect grows to
    SIZE_MOD_IMPLOSION = 5				#The size multiplier the Implosion Effect grows to
    SIZE_MOD_MELEE = 1.5				#The size multiplier the Melee Effect grows to
    TIME_EXPLOSION = 0.2				#The time the Explosion Effect lasts
    TIME_EXPLOSION_VERTICAL = 0.5			#The time the Explosion Vertical Effect lasts
    TIME_HEALTH_BAR = 3					#The time the Health Bar Effect lasts
    TIME_IMPLOSION = 0.5				#The time the Implosion Effect lasts
    TIME_MANA_BAR = 3					#The time the Mana Bar Effect lasts
    TIME_MELEE = 0.5					#The time the Melee Effect lasts
    TRANSPARENCY_EXPLOSION = 150			#The initial transparency of the Explosion Effect
    TRANSPARENCY_EXPLOSION_VERTICAL = 150		#The initial transparency of the Explosion Vertical Effect
    TRANSPARENCY_IMPLOSION = 150			#The initial transparency of the Implosion Effect
    TRANSPARENCY_MELEE = 150				#The initial transparency of the Melee Effect

    #Define the constructor
    def __init__(self, width, height, posX, posY, dirX, dirY, imageString, type):
        super().__init__(NodeType.EFFECT, width, height, posX, posY, 0, dirX, dirY, imageString, -1, "Effect")

        #Set Node fields
        self.type = type				#The Effect type

        #Set Effect fields
        self.entity = None				#The referenced Entity
        self.heightOriginal = height			#The Effects original height
        self.timeLeft = -1				#The Effects timeLeft
        self.widthOriginal = width			#The Effects original width

        #Depending on the Effect type, set timeLeft etc.
        if self.type is EffectType.EXPLOSION:
            self.timeLeft = self.TIME_EXPLOSION
        elif self.type is EffectType.EXPLOSION_VERTICAL:
            self.timeLeft = self.TIME_EXPLOSION_VERTICAL
        elif self.type is EffectType.HEALTH_BAR:
            self.timeLeft = self.TIME_HEALTH_BAR
            self.setColour(self.COLOUR_HEALTH_BAR[0], self.COLOUR_HEALTH_BAR[1], self.COLOUR_HEALTH_BAR[2])
        elif self.type is EffectType.IMPLOSION:
            self.timeLeft = self.TIME_IMPLOSION
        elif self.type is EffectType.MANA_BAR:
            self.timeLeft = self.TIME_MANA_BAR
            self.setColour(self.COLOUR_MANA_BAR[0], self.COLOUR_MANA_BAR[1], self.COLOUR_MANA_BAR[2])
        elif self.type is EffectType.MELEE:
            self.timeLeft = self.TIME_MELEE
        elif self.type is EffectType.RETICLE:
            self.timeLeft = -1
            self.setColour(self.COLOUR_RETICLE[0], self.COLOUR_RETICLE[1], self.COLOUR_RETICLE[2])

    #Define a Explosion Effect factory
    def Explosion(width, height, posX, posY):
        return Effect(width, height, posX, posY, 0, 0, Effect.IMAGE_EXPLOSION, EffectType.EXPLOSION)

    #Define a Explosion Vertical Effect factory
    def ExplosionVertical(width, height, posX, posY):
        return Effect(width, height, posX, posY, 0, 0, Effect.IMAGE_EXPLOSION_VERTICAL, EffectType.EXPLOSION_VERTICAL)

    #Define a Implosion Effect factory
    def Implosion(width, height, posX, posY):
        return Effect(width, height, posX, posY, 0, 0, Effect.IMAGE_IMPLOSION, EffectType.IMPLOSION)

    #Define a Health Bar Effect factory
    def HealthBar(width, height, posX, posY):
        return Effect(width, height, posX, posY, 0, 0, Effect.IMAGE_HEALTH_BAR, EffectType.HEALTH_BAR)

    #Define a Mana Bar Effect factory
    def ManaBar(width, height, posX, posY):
        return Effect(width, height, posX, posY, 0, 0, Effect.IMAGE_MANA_BAR, EffectType.MANA_BAR)

    #Define a Melee Effect factory
    def Melee(width, height, posX, posY, dirX, dirY):
        return Effect(width, height, posX, posY, dirX, dirY, Effect.IMAGE_MELEE, EffectType.MELEE)

    #Define a Reticle Effect factory
    def Reticle(width, height, posX, posY):
        return Effect(width, height, posX, posY, 0, 0, Effect.IMAGE_RETICLE, EffectType.RETICLE)

    #Reset timeLeft depending on the Effect type
    def resetTimeLeft(self):
        if self.type is EffectType.HEALTH_BAR:
            self.timeLeft = self.TIME_HEALTH_BAR

    #Update the Effect status
    def update(self, frameDeltaTime):
        self.timeLeft -= frameDeltaTime

        #If the Effect has expired, return true
        if self.timeLeft < 0:
            return True

        #Depending on the Effect type
        if self.type is EffectType.EXPLOSION:
            #Calculate new size/transparency
            newWidth = int(self.widthOriginal * (1 + self.SIZE_MOD_EXPLOSION * (self.TIME_EXPLOSION - self.timeLeft) / self.TIME_EXPLOSION))
            newHeight = int(self.heightOriginal * (1 + self.SIZE_MOD_EXPLOSION * (self.TIME_EXPLOSION - self.timeLeft) / self.TIME_EXPLOSION))
            newTransparency = int(self.TRANSPARENCY_EXPLOSION * self.timeLeft / self.TIME_EXPLOSION)

            #Set new size/transparency
            self.setSize(newWidth, newHeight)
            self.setTransparency(newTransparency)
        elif self.type is EffectType.EXPLOSION_VERTICAL:
            #Calculate new size/transparency
            newHeight = int(self.heightOriginal * (1 + self.SIZE_MOD_EXPLOSION_VERTICAL * (self.TIME_EXPLOSION_VERTICAL - self.timeLeft) / self.TIME_EXPLOSION_VERTICAL))
            newTransparency = int(self.TRANSPARENCY_EXPLOSION_VERTICAL * self.timeLeft / self.TIME_EXPLOSION_VERTICAL)

            #Set new size/transparency
            self.setSize(self.width, newHeight)
            self.setTransparency(newTransparency)
        elif self.type is EffectType.IMPLOSION:
            #Calculate new size/transparency
            newWidth = int(self.widthOriginal * (1 + self.SIZE_MOD_IMPLOSION * self.timeLeft / self.TIME_IMPLOSION))
            newHeight = int(self.heightOriginal * (1 + self.SIZE_MOD_IMPLOSION * self.timeLeft / self.TIME_IMPLOSION))
            newTransparency = int(self.TRANSPARENCY_IMPLOSION * self.timeLeft / self.TIME_IMPLOSION)

            #Set new size/transparency
            self.setSize(newWidth, newHeight)
            self.setTransparency(newTransparency)
        elif self.type is EffectType.MELEE:
            #Calculate new size/transparency
            newTransparency = int(self.TRANSPARENCY_MELEE * self.timeLeft / self.TIME_MELEE)
            newWidth = int(self.widthOriginal * (1 + self.SIZE_MOD_MELEE * (self.TIME_MELEE - self.timeLeft) / self.TIME_MELEE))

            #Move the Effect in the direction of travel so it appears not to move but expand in a direction
            if self.direction.x < 0:
                self.position.x = self.position.x + ((self.width - newWidth) // 2)
            elif self.direction.x > 0:
                self.position.x = self.position.x - ((self.width - newWidth) // 2)

            #Set new size/transparency
            self.setSize(newWidth, self.height)
            self.setTransparency(newTransparency)

        return False



