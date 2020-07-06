#!/usr/bin/python

#Import libraries
import pygame
from pygame.locals import *

from effect import *
from entity import *

#Define a class for the GUI
class GUI(Node):
    HEIGHT_HEALTH_BAR = 0.025
    HEIGHT_MANA_BAR = 0.025
    IMAGE_MELEE = "./resources/hud_melee.png"
    IMAGE_RANGED = "./resources/hud_ranged.png"
    IMAGE_SPELL = "./resources/hud_spell.png"
    IMAGE_SUMMON = "./resources/hud_summon.png"
    POSITION_X_ATTACK_STYLE = 0.825
    POSITION_X_ATTACK_TYPE = 0.075
    POSITION_X_HEALTH_BAR = 0.25
    POSITION_X_MANA_BAR = 0.25
    POSITION_Y_ATTACK_STYLE = 0.8
    POSITION_Y_ATTACK_TYPE = 0.8
    POSITION_Y_HEALTH_BAR = 0.9
    POSITION_Y_MANA_BAR = 0.87
    SIZE_ATTACK_STYLE = 0.1
    SIZE_ATTACK_TYPE = 0.1
    WIDTH_HEALTH_BAR = 0.5
    WIDTH_MANA_BAR = 0.5

    #Define the constructor
    def __init__(self, width, height):

        #Set GUI fields
        self.aspectRatio = width / height
        self.height = height
        self.heightHalf = height // 2
        self.width = width
        self.widthHalf = width // 2

        #Initialize GUI fields
        self.nodes = []
        self.selectionTimeLeft = -1

        #Declare GUI pointers
        self.attackTypeReadout = None
        #self.attackTypeReadoutNext = None
        #self.attackTypeReadoutPrevious = None
        self.attackTypeValue = None
        self.attackStyleReadout = None
        #self.attackStyleReadoutNext = None
        #self.attackStyleReadoutPrevious = None
        self.attackStyleValue = None

        #Create health/mana readouts
        self.healthReadout = Effect.HealthBar(int(self.width * self.WIDTH_HEALTH_BAR), int(self.height * self.HEIGHT_HEALTH_BAR), int(self.width * self.POSITION_X_HEALTH_BAR), int(self.height * self.POSITION_Y_HEALTH_BAR))
        self.manaReadout = Effect.ManaBar(int(self.width * self.WIDTH_MANA_BAR), int(self.height * self.HEIGHT_MANA_BAR), int(self.width * self.POSITION_X_MANA_BAR), int(self.height * self.POSITION_Y_MANA_BAR))
        self.nodes.append(self.healthReadout)
        self.nodes.append(self.manaReadout)

        #Create attackType readout
        self.attackTypeReadout = Node.Node(int(self.width * self.SIZE_ATTACK_TYPE), int(self.height * self.SIZE_ATTACK_TYPE * self.aspectRatio), int(self.width * self.POSITION_X_ATTACK_TYPE), int(self.height * self.POSITION_Y_ATTACK_TYPE), self.IMAGE_MELEE)
        self.nodes.append(self.attackTypeReadout)

        #Create attackStyle readout
        self.attackStyleReadout = Node.Node(int(self.width * self.SIZE_ATTACK_STYLE), int(self.height * self.SIZE_ATTACK_STYLE * self.aspectRatio), int(self.width * self.POSITION_X_ATTACK_STYLE), int(self.height * self.POSITION_Y_ATTACK_STYLE), self.IMAGE_MELEE)
        self.nodes.append(self.attackStyleReadout)

    #Update the GUI
    def update(self, player, frameDeltaTime):
        self.selectionTimeLeft -= frameDeltaTime

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



