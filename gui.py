#!/usr/bin/python

#Import libraries
import pygame
from pygame.locals import *

from entity import *

#Define a class for the GUI
class GUI(Node):
    IMAGE_HEALTH_BAR = "../resources/mine/square.png"
    IMAGE_MANA_BAR = "../resources/mine/square.png"
    HEIGHT_HEALTH_BAR = 0.05
    HEIGHT_MANA_BAR = 0.05
    POSITION_X_HEALTH_BAR = 0.25
    POSITION_X_MANA_BAR = 0.25
    POSITION_Y_HEALTH_BAR = 0.85
    POSITION_Y_MANA_BAR = 0.8
    WIDTH_HEALTH_BAR = 0.5
    WIDTH_MANA_BAR = 0.5

    #Define the constructor
    def __init__(self, width, height):

        #Set GUI fields
        self.height = height
        self.heightHalf = height // 2
        self.width = width
        self.widthHalf = width // 2

        #Initialize GUI fields
        self.nodes = []

        #Set GUI pointers
        self.healthReadout = Node(NodeType.EFFECT, int(self.width * self.WIDTH_HEALTH_BAR), int(self.height * self.HEIGHT_HEALTH_BAR), int(self.width * self.POSITION_X_HEALTH_BAR), int(self.height * self.POSITION_Y_HEALTH_BAR), 0, 0, 0, self.IMAGE_HEALTH_BAR, -1)
        self.manaReadout = Node(NodeType.EFFECT, int(self.width * self.WIDTH_MANA_BAR), int(self.height * self.HEIGHT_MANA_BAR), int(self.width * self.POSITION_X_MANA_BAR), int(self.height * self.POSITION_Y_MANA_BAR), 0, 0, 0, self.IMAGE_MANA_BAR, -1)

        #Add health/mana readouts to the GUI nodes array
        self.nodes.append(self.healthReadout)
        self.nodes.append(self.manaReadout)

    #Update the GUI
    def update(self, player, frameDeltaTime):
        #If there is a player, update the health/mana bar
        if player:
            self.healthReadout.setWidth(int(self.WIDTH_HEALTH_BAR * player.getHealthPercentage()))
            self.manaReadout.setWidth(int(self.WIDTH_MANA_BAR * player.getManaPercentage()))

        pass



