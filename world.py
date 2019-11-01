#!/usr/bin/python

#Import libraries
from ammo import *
from entity import *
from terrain import *

#Define a class for World, which manages all Nodes in a locale
class World:
    FRICTION = 49.5
    GRAVITY = 100
    MAX_SPEED = 100 #TODO

    #Define the constructor
    def __init__(self, name, seedValue):
        self.name = name
        self.seedValue = seedValue

        self.friction = 100
        self.gravity = 100
        self.maxSpeed = 100

        self.ammo = []
        self.entitys = []
        self.terrain = []

        self.createWorld()

    #Create a World based on the seedValue
    def createWorld(self):
        #TODO implement properly

        #Add some Terrain
        for i in range(-5, 6):
            self.terrain.append(Terrain(i * Terrain.TERRAIN_SIZE, Terrain.TERRAIN_SIZE, "../resources/mine2/test.png"))
        for i in range(3, 6):
            self.terrain.append(Terrain(i * Terrain.TERRAIN_SIZE, - 2 * Terrain.TERRAIN_SIZE, "../resources/mine2/test.png"))
        self.terrain.append(Terrain(-5 * Terrain.TERRAIN_SIZE, 0, "../resources/mine2/test.png"))
        self.terrain.append(Terrain(5 * Terrain.TERRAIN_SIZE, 0, "../resources/mine2/test.png"))

        #Add an Entity
        self.world.entitys.append(Entity(100, 100, 0, 0, 0, 0, 0, "../resources/mine/circle.png"))

    #Apply gravity to an Entity depending on what if any Terrain it is on
    def entityApplyGravity(self, entity, frameDeltaTime):
        onTerrain = False

        #Calculate facts about the Entity position used for detecting whether the Entity is on solid Terrain
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
            #Otherwise the Entity is on the Terrain, ensure the Entitys height and return True
            else:
                entity.position.y = node.position.y - entity.height
                entity.direction = Vector2f(0, 0)
                entity.state = EntityState.MOVING
                onTerrain = True
                break

        #If the Entity isn't on Terrain, apply gravity to the Entity
        if not onTerrain:
            entity.accelerate(0, self.GRAVITY * frameDeltaTime)

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

    #Update the World, apply Gravity, Direction etc.
    def update(self, frameDeltaTime):
        #For all Entitys, apply Gravity, apply Direction, Update
        for node in self.entitys:
            self.entityApplyGravity(node, frameDeltaTime)
            self.entityMove(node, node.direction.x * frameDeltaTime, node.direction.y * frameDeltaTime)
            node.update(frameDeltaTime)



