#!/usr/bin/python

#Import libraries
import pygame
from pygame.locals import *

from effect import *
from entity import *

#Define a class for the GUI
class GUI(Node):
    HEIGHT_HEALTH_BAR = 0.025				#The height of the Health Bar readout
    HEIGHT_MANA_BAR = 0.025				#The height of the Mana Bar readout
    IMAGE_MELEE = "./resources/hud_melee.png"		#The image for the Melee Attack Type
    IMAGE_RANGED = "./resources/hud_ranged.png"		#The image for the Ranged Attack Type
    IMAGE_SPELL = "./resources/hud_spell.png"		#The image for the Spell Attack Type
    IMAGE_SUMMON = "./resources/hud_summon.png"		#The image for the Summon Attack Type
    POSITION_X_ATTACK_STYLE = 0.825			#The x position of the Attack Style readout
    POSITION_X_ATTACK_TYPE = 0.075			#The x position of the Attack Type readout
    POSITION_X_HEALTH_BAR = 0.25			#The x position of the Health Bar readout
    POSITION_X_MANA_BAR = 0.25				#The x position of the Mana Bar readout
    POSITION_Y_ATTACK_STYLE = 0.8			#The y position of the Attack Style readout
    POSITION_Y_ATTACK_TYPE = 0.8			#The y position of the Attack Type readout
    POSITION_Y_HEALTH_BAR = 0.9				#The y position of the Health Bar readout
    POSITION_Y_MANA_BAR = 0.87				#The y position of the Mana Bar readout
    SIZE_ATTACK_STYLE = 0.1				#The size of the Attack Style readout
    SIZE_ATTACK_TYPE = 0.1				#The size of the Attack Type readout
    WIDTH_HEALTH_BAR = 0.5				#The width of the Health Bar readout
    WIDTH_MANA_BAR = 0.5				#The width of the Mana Bar readout

    #Define the constructor
    def __init__(self, width, height):

        #Set GUI fields
        self.aspectRatio = width / height		#The aspect ratio of the GUI
        self.height = height				#The screen height
        self.heightHalf = height // 2			#The screen height halved
        self.width = width				#The screen width
        self.widthHalf = width // 2			#The screen width halved

        #Initialize GUI fields
        self.nodes = []					#The Nodes in the GUI

        #Declare GUI pointers
        self.attackStyleReadout = None			#The current attackStyle readout
        #self.attackStyleReadoutNext = None		#The next attackStyle readout
        #self.attackStyleReadoutPrevious = None		#The previous attackStyle readout
        self.attackStyleValue = None			#The current attackStyle value
        self.attackTypeReadout = None			#The current attackType readout
        #self.attackTypeReadoutNext = None		#The next attackType readout
        #self.attackTypeReadoutPrevious = None		#The previous attackType readout
        self.attackTypeValue = None			#The current attackType value
        self.healthReadout = None			#The health readout
        self.manaReadout = None				#The mana readout

        #Create attackStyle/attackType readouts
        self.attackStyleReadout = Node.Node(int(self.width * self.SIZE_ATTACK_STYLE), int(self.height * self.SIZE_ATTACK_STYLE * self.aspectRatio), int(self.width * self.POSITION_X_ATTACK_STYLE), int(self.height * self.POSITION_Y_ATTACK_STYLE), self.IMAGE_MELEE)
        self.attackTypeReadout = Node.Node(int(self.width * self.SIZE_ATTACK_TYPE), int(self.height * self.SIZE_ATTACK_TYPE * self.aspectRatio), int(self.width * self.POSITION_X_ATTACK_TYPE), int(self.height * self.POSITION_Y_ATTACK_TYPE), self.IMAGE_MELEE)
        self.nodes.append(self.attackStyleReadout)
        self.nodes.append(self.attackTypeReadout)

        #Create health/mana readouts
        self.healthReadout = Effect.HealthBar(int(self.width * self.WIDTH_HEALTH_BAR), int(self.height * self.HEIGHT_HEALTH_BAR), int(self.width * self.POSITION_X_HEALTH_BAR), int(self.height * self.POSITION_Y_HEALTH_BAR))
        self.manaReadout = Effect.ManaBar(int(self.width * self.WIDTH_MANA_BAR), int(self.height * self.HEIGHT_MANA_BAR), int(self.width * self.POSITION_X_MANA_BAR), int(self.height * self.POSITION_Y_MANA_BAR))
        self.nodes.append(self.healthReadout)
        self.nodes.append(self.manaReadout)

    #Update the GUI
    def update(self, player, frameDeltaTime):
        #If there is a player, update the health/mana bar
        if player:
            self.healthReadout.setWidth(int(self.width * self.WIDTH_HEALTH_BAR * player.getHealthPercentage()))
            self.manaReadout.setWidth(int(self.width * self.WIDTH_MANA_BAR * player.getManaPercentage()))

            #If the Player attackStyle is different from the GUI, update the GUI
            if self.attackStyleValue is not player.attackStyle:
                self.attackStyleValue = player.attackStyle

                #Depending on the AttackStyle set the image
                if self.attackStyleValue is AttackType.MELEE:
                    self.attackStyleReadout.setImage(self.IMAGE_MELEE)
                elif self.attackStyleValue is AttackType.RANGED:
                    self.attackStyleReadout.setImage(self.IMAGE_RANGED)
                elif self.attackStyleValue is AttackType.SPELL:
                    self.attackStyleReadout.setImage(self.IMAGE_SPELL)
                elif self.attackStyleValue is AttackType.SUMMON:
                    self.attackStyleReadout.setImage(self.IMAGE_SUMMON)

            #If the Player attackType is different from the GUI, update the GUI
            if self.attackTypeValue is not player.attackType:
                self.attackTypeValue = player.attackType

                #Depending on the AttackType set the image
                if self.attackTypeValue is AttackType.MELEE:
                    self.attackTypeReadout.setImage(self.IMAGE_MELEE)
                elif self.attackTypeValue is AttackType.RANGED:
                    self.attackTypeReadout.setImage(self.IMAGE_RANGED)
                elif self.attackTypeValue is AttackType.SPELL:
                    self.attackTypeReadout.setImage(self.IMAGE_SPELL)
                elif self.attackTypeValue is AttackType.SUMMON:
                    self.attackTypeReadout.setImage(self.IMAGE_SUMMON)



