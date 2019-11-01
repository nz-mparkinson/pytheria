#!/usr/bin/python

#Import libraries
import random

from ammo import *
from entity import *
from terrain import *

#Define a class for World, which manages all Nodes in a locale
class World:
    FRICTION_DEFAULT = 49.5
    GRAVITY_DEFAULT = 100
    MAX_SPEED_DEFAULT = 100 #TODO implement
    WORLD_HEIGHT_DEFAULT = 16
    WORLD_HEIGHT_DEFAULT_WIDTH = 4
    WORLD_HEIGHT_MAX = 24 #TODO not used
    WORLD_HEIGHT_MIN = 8 #TODO not used
    WORLD_HEIGHT_STEP_MAX = 2
    WORLD_WIDTH = 16

    #Define the constructor
    def __init__(self, name, seedValue):
        self.name = name
        self.seedValue = seedValue

        self.ammo = []
        self.entitys = []
        self.terrain = []

        self.createWorld()

    #Create a World based on the seedValue
    def createWorld(self):
        #Set physics values
        self.friction = self.FRICTION_DEFAULT
        self.gravity = self.GRAVITY_DEFAULT
        self.maxSpeed = self.MAX_SPEED_DEFAULT

        #Add Terrain around the Player at the default height
        for i in range(-self.WORLD_HEIGHT_DEFAULT_WIDTH, self.WORLD_HEIGHT_DEFAULT_WIDTH):
            for j in range(-self.WORLD_HEIGHT_DEFAULT, 0):
                self.terrain.append(Terrain(i * Terrain.TERRAIN_SIZE, -j * Terrain.TERRAIN_SIZE, "../resources/mine2/test.png"))

        #Seed the random number generator
        random.seed(self.seedValue)

        #Add Terrain with random heights to the right of the Player
        terrainHeight = 0
        for i in range(self.WORLD_HEIGHT_DEFAULT_WIDTH, self.WORLD_WIDTH):
            terrainHeight = terrainHeight + random.randrange(-self.WORLD_HEIGHT_STEP_MAX, self.WORLD_HEIGHT_STEP_MAX+1)
            print(terrainHeight)
            for j in range(-self.WORLD_HEIGHT_DEFAULT, terrainHeight):
                self.terrain.append(Terrain(i * Terrain.TERRAIN_SIZE, -j * Terrain.TERRAIN_SIZE, "../resources/mine2/test.png"))

        #Add Terrain with random heights to the left of the Player
        terrainHeight = 0
        for i in reversed(range(-self.WORLD_WIDTH, -self.WORLD_HEIGHT_DEFAULT_WIDTH)):
            terrainHeight = terrainHeight + random.randrange(-self.WORLD_HEIGHT_STEP_MAX, self.WORLD_HEIGHT_STEP_MAX+1)
            #print(terrainHeight)
            for j in range(-self.WORLD_HEIGHT_DEFAULT, terrainHeight):
                self.terrain.append(Terrain(i * Terrain.TERRAIN_SIZE, -j * Terrain.TERRAIN_SIZE, "../resources/mine2/test.png"))

        #Add an Entity
        self.entitys.append(Entity(100, 100, 0, 0, 0, 0, 0, "../resources/mine/circle.png"))

    #Apply gravity to an Entity depending on what if any Terrain it is on
    def entityApplyGravity(self, entity, frameDeltaTime):
        #Get the Terrain the Entity is on if any
        onTerrain = None
        onTerrain = self.isEntityOnTerrain(entity)

        #If the Entity is on Terrain, ensure the Entitys height
        if onTerrain:
            entity.position.y = onTerrain.position.y - entity.height
            entity.direction = Vector2f(0, 0)
            entity.state = EntityState.MOVING
        #Otherwise, apply gravity to the Entity
        else:
            entity.accelerate(0, self.GRAVITY_DEFAULT * frameDeltaTime)

    #Move an Entity
    def entityMove(self, entity, x, y):
        #Calculate facts about the Entity position used for detecting whether the Entity will collide with solid Terrain
        entityYTop = y + entity.position.y
        entityYBottom = y + entity.position.y + entity.height
        entityXLeft = x + entity.position.x
        entityXRight = x + entity.position.x + entity.width

        #For all Terrain
        for node in self.terrain:
            #Skip if the Entity is too far left
            if node.position.x + node.width <= entityXLeft:
                pass
            #Skip if the Entity is too far right
            elif node.position.x >= entityXRight:
                pass
            #Skip if the Entity is too far up
            elif node.position.y + node.height <= entityYTop:
                pass
            #Skip if the Entity is too far down
            elif node.position.y >= entityYBottom:
                pass
            #Otherwise the Entity will collide with the Terrain, handle accordlingly, note: setting values exactly due to float rounding
            else:
                #If the Entity is moving too far left
                if node.position.x + node.width > entityXLeft and x < 0:
                    x = node.position.x + node.width - entity.position.x
                #If the Entity is moving too far right
                elif node.position.x < entityXRight and x > 0:
                    x = node.position.x - entity.position.x - entity.width
                #If the Entity is moving too far up
                elif node.position.y + node.height > entityYTop and y < 0:
                    y = node.position.y + node.height - entity.position.y
                #If the Entity is moving too far down
                elif node.position.y < entityYBottom and y > 0:
                    y = node.position.y - entity.position.y - entity.height

        #If x or y are non 0, move the Entity
        if x != 0 or y != 0:
            entity.move(x, y)

    #Test whether the Entity is on Terrain, returns the Terrain if it is, else None
    def isEntityOnTerrain(self, entity):
        #Calculate facts about the Entity position used for detecting whether the Entity is on solid Terrain
        #TODO magic values
        entityYTop = entity.position.y + entity.height * 0.5
        entityYBottom = entity.position.y + entity.height
        entityXLeft = entity.position.x + entity.width * 0.25
        entityXRight = entity.position.x + entity.width * 0.75

        #For all Terrain
        for node in self.terrain:
            #Skip if the Entity is too far left
            if node.position.x + node.width < entityXLeft:
                pass
            #Skip if the Entity is too far right
            elif node.position.x > entityXRight:
                pass
            #Skip if the Entity is too far up
            elif node.position.y + node.height < entityYTop:
                pass
            #Skip if the Entity is too far down
            elif node.position.y > entityYBottom:
                pass
            #Otherwise the Entity is on the Terrain, return the Terrain
            else:
                return node

        return None

    #Update the World, apply Gravity, Direction etc.
    def update(self, frameDeltaTime):
        #For all Entitys, apply Gravity, apply Direction, Update
        for node in self.entitys:
            self.entityApplyGravity(node, frameDeltaTime)
            self.entityMove(node, node.direction.x * frameDeltaTime, node.direction.y * frameDeltaTime)
            node.update(frameDeltaTime)



