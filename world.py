#!/usr/bin/python

#Import libraries
import random

from ammo import *
from entity import *
from terrain import *

#Define a class for World, which manages all Nodes in a locale
class World:
    FRICTION_DEFAULT = 50
    GRAVITY_DEFAULT = 200
    MAX_SPEED_DEFAULT = 400 #TODO implement
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

        self.collidables = []
        self.selectables = []

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
                self.addTerrain(Terrain(i * Terrain.TERRAIN_SIZE, -j * Terrain.TERRAIN_SIZE, "../resources/mine2/test.png"))

        #Seed the random number generator
        random.seed(self.seedValue)

        #Add Terrain with random heights to the right of the Player
        terrainHeight = 0
        for i in range(self.WORLD_HEIGHT_DEFAULT_WIDTH, self.WORLD_WIDTH):
            terrainHeight = terrainHeight + random.randrange(-self.WORLD_HEIGHT_STEP_MAX, self.WORLD_HEIGHT_STEP_MAX+1)
            for j in range(-self.WORLD_HEIGHT_DEFAULT, terrainHeight):
                self.addTerrain(Terrain(i * Terrain.TERRAIN_SIZE, -j * Terrain.TERRAIN_SIZE, "../resources/mine2/test.png"))

        #Add Terrain with random heights to the left of the Player
        terrainHeight = 0
        for i in reversed(range(-self.WORLD_WIDTH, -self.WORLD_HEIGHT_DEFAULT_WIDTH)):
            terrainHeight = terrainHeight + random.randrange(-self.WORLD_HEIGHT_STEP_MAX, self.WORLD_HEIGHT_STEP_MAX+1)
            for j in range(-self.WORLD_HEIGHT_DEFAULT, terrainHeight):
                self.addTerrain(Terrain(i * Terrain.TERRAIN_SIZE, -j * Terrain.TERRAIN_SIZE, "../resources/mine2/test.png"))

        #Add an enemy Entity
        self.addEntity(Entity(Entity.WIDTH_DEFAULT, Entity.HEIGHT_DEFAULT, 50, 0, 0, 0, 0, "../resources/mine/circle.png", 1))

    #Add an Ammo to the World
    def addAmmo(self, node):
        self.ammo.append(node)

    #Add an Entity to the World
    def addEntity(self, node):
        self.entitys.append(node)
        self.collidables.append(node)   #TODO doesn't work
        self.selectables.append(node)   #TODO doesn't work

    #Add an Terrain to the World
    def addTerrain(self, node):
        self.terrain.append(node)
        self.collidables.append(node)   #TODO doesn't work
        self.selectables.append(node)   #TODO doesn't work

    #Handle a Ammo collision with an enemy 
    def ammoCollisionEnemy(self, ammo, enemy):
        #TODO handle ammo collision with En
        pass

    #Run Entity AI
    def entityAI(self, entity, frameDeltaTime):
        #Find the closest enemy
        enemy = self.getClosestEntity(entity, None, entity.team)

        #If an enemy was found
        if enemy:
            #Get its relative positon
            relativePosition = enemy.position - entity.position

            #Move towards it
            if relativePosition.x < 0:
                self.nodeMove(entity, -entity.speed * frameDeltaTime, 0)
            else:
                self.nodeMove(entity, entity.speed * frameDeltaTime, 0)

            #TODO if in range
            self.entityAttackMelee(entity)

            #Jump
            self.entityJump(entity)

    #Have an Entity Attack using Melee TODO
    def entityAttackMelee(self, entity):
        #Find the closest enemy
        enemy = self.getClosestEntity(entity, entity.attackRange, entity.team)

        #TODO if hit
        if enemy:
            self.entityDamage(enemy, entity.attackDamage)

    #Have an Entity Attack using Ranged TODO
    def entityAttackRanged(self, entity, dirX, dirY):
        self.addAmmo(Ammo(entity.getCentreX(), entity.getCentreY(), dirX, dirY, "../resources/mine/circle.png", AmmoType.RANGED, entity.team, entity.rangedRange, entity.rangedSpeed))

    #Have an Entity Attack using Spell TODO
    def entityAttackSpell(self, entity, dirX, dirY):
        #TODO when using Entity centre, the targeting is off
        self.addAmmo(Ammo(entity.position.x, entity.position.y, dirX, dirY, "../resources/mine/circle.png", AmmoType.SPELL, entity.team, entity.spellRange, entity.spellSpeed))

    #Apply Damage to an Entity
    def entityDamage(self, entity, damage):
        entity.damage(damage)

    #Apply Gravity to an Entity depending on what if any Terrain it is on
    def entityGravity(self, entity, frameDeltaTime):
        #Get the Terrain the Entity is on if any
        onTerrain = None
        onTerrain = self.isEntityOnTerrain(entity)

        #If the Entity is on Terrain, ensure the Entitys vertical position and direction
        if onTerrain:
            entity.position.y = onTerrain.position.y - entity.height
            entity.direction.y = 0
        #Otherwise, apply gravity to the Entity
        else:
            entity.accelerate(0, self.GRAVITY_DEFAULT * frameDeltaTime)

    #Have an Entity Jump
    def entityJump(self, entity):
        #If the Entity is on Terrain, jump
        if self.isEntityOnTerrain(entity):
            self.nodeMove(entity, entity.direction.x, -entity.getJumpHeight())
            entity.direction.y = 0
            #entity.jump()

    #Get the closest Entity optionally with range and not belonging to the same team
    def getClosestEntity(self, entity, range, team):
        closestDistanceSQ = 0
        closestEntity = None

        #For all Entitys, find the closest
        for node in self.entitys:
            if team is None or node.team != team:
                if closestEntity is None or closestDistanceSQ > entity.position.getLengthToSQ(node.position):
                    if range is None or range * range >= entity.position.getLengthToSQ(node.position):
                        closestEntity = node
                        closestDistanceSQ = entity.position.getLengthToSQ(node.position)

        return closestEntity

    #Get the closest Node thats selectable, optionally with range
    def getClosestNode(self, entity, range):
        closestDistanceSQ = 0
        closestNode = None

        #For all selectable Nodes, find the closest
        for node in self.selectable:
            if closestEntity is None or closestDistanceSQ > entity.position.getLengthToSQ(node.position):
               if range is None or range * range >= entity.position.getLengthToSQ(node.position):
                   closestNode = node
                   closestDistanceSQ = entity.position.getLengthToSQ(node.position)

        return closestNode

    #Test whether the Entity is on Terrain, returns the Terrain if it is, else None
    def isEntityOnTerrain(self, entity):
        #Calculate facts about the Entity position used for detecting whether the Entity is on solid Terrain, note: +/- 1 because of floating points
        #TODO magic values
        entityYTop = entity.position.y + entity.height * 0.5 -1
        entityYBottom = entity.position.y + entity.height +1
        entityXLeft = entity.position.x + entity.width * 0.25 -1
        entityXRight = entity.position.x + entity.width * 0.75 +1

        #For all Terrain
        for node in self.terrain:
            #Skip if the Entity is too far left
            if node.position.x + node.width < entityXLeft:
                pass
            #Skip if the Entity is too far right
            elif node.position.x > entityXRight:
                pass
            #Skip if the Entity is too far down
            elif node.position.y + node.height < entityYTop:
                pass
            #Skip if the Entity is too far up
            elif node.position.y > entityYBottom:
                pass
            #Otherwise the Entity is on the Terrain, return the Terrain
            else:
                return node

        return None

    #Move a Node
    def nodeMove(self, node, x, y):
        #Calculate facts about the Node position used for detecting whether the Node will collide with the Collidable
        nodeYTop = y + node.position.y
        nodeYBottom = y + node.position.y + node.height
        nodeXLeft = x + node.position.x
        nodeXRight = x + node.position.x + node.width

        #For all Collidable nodes
        for collidable in self.terrain:
            #Skip if the Node is a Entity
            #if collidable.nodeType is NodeType.ENTITY and node.nodeType is NodeType.ENTITY:
            #    pass
            #Skip if the Node is too far left
            if collidable.position.x + collidable.width <= nodeXLeft:
                pass
            #Skip if the Node is too far right
            elif collidable.position.x >= nodeXRight:
                pass
            #Skip if the Node is too far down
            elif collidable.position.y + collidable.height <= nodeYTop:
                pass
            #Skip if the Node is too far up
            elif collidable.position.y >= nodeYBottom:
                pass
            #Otherwise the Node will collide with the Collidable, handle accordlingly, note: setting values exactly due to float rounding
            else:
                #Calculate how close the Node is to each edge of the Node
                leftDelta = abs(collidable.position.x + collidable.width - node.position.x)
                rightDelta = abs(collidable.position.x - node.position.x - node.width)
                upDelta = abs(collidable.position.y + collidable.height - node.position.y)
                downDelta = abs(collidable.position.y - node.position.y - node.height)

                #If the Node is moving too far left, set its horizontal position and direction
                if leftDelta < rightDelta and leftDelta < upDelta and leftDelta < downDelta:
                    x = collidable.position.x + collidable.width - node.position.x
                    node.direction.x = 0
                #If the Node is moving too far right, set its horizontal position and direction
                elif rightDelta < leftDelta and rightDelta < upDelta and rightDelta < downDelta:
                    x = collidable.position.x - node.position.x - node.width
                    node.direction.x = 0
                #If the Node is moving too far up, set its vertical position and direction
                elif upDelta < leftDelta and upDelta < rightDelta and upDelta < downDelta:
                    y = collidable.position.y + collidable.height - node.position.y
                    node.direction.y = 0
                #If the Node is moving too far down, set its vertical position and direction
                elif downDelta < leftDelta and downDelta < rightDelta and downDelta < upDelta:
                    y = collidable.position.y - node.position.y - node.height
                    node.direction.y = 0

        #If x or y are non 0, move the Node
        if x != 0 or y != 0:
            node.move(x, y)

    #Remove an Ammo from the World
    def removeAmmo(self, node):
        self.ammo.remove(node)

    #Remove an Entity from the World
    def removeEntity(self, node):
        self.entitys.remove(node)
        self.collidables.remove(node)
        self.selectables.remove(node)

    #Remove an Terrain from the World
    def removeTerrain(self, node):
        self.terrain.remove(node)
        self.collidables.remove(node)
        self.selectables.remove(node)

    #Update the World, apply Gravity, Direction etc.
    def update(self, player, frameDeltaTime):
        #For all Entitys
        for node in self.entitys:
            #If the Entity has expired, remove it
            if node.update(frameDeltaTime):
                self.entitys.remove(node)

            #Apply Gravity, Direction
            self.entityGravity(node, frameDeltaTime)
            self.nodeMove(node, node.direction.x * frameDeltaTime, node.direction.y * frameDeltaTime)

            #If the Entity isn't the Player, runAI
            if node is not player:
                self.entityAI(node, frameDeltaTime)

        #For all Ammo
        for node in self.ammo:
            #If the Ammo has expired, remove it
            if node.update(frameDeltaTime):
                self.ammo.remove(node)

            #If the Ammo type is Ranged, apply Gravity
            if node.type is AmmoType.RANGED:
                self.entityGravity(node, frameDeltaTime)
            #Apply Direction
            self.nodeMove(node, node.direction.x * frameDeltaTime, node.direction.y * frameDeltaTime)

        #For all Terrain, Update
        for node in self.terrain:
            node.update(frameDeltaTime)



