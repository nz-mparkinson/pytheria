#!/usr/bin/python

#Import libraries
import random

from ammo import *
from effect import *
from entity import *
from terrain import *

#Define a class for World, which manages all Nodes in a locale
class World:
    #GUI
    HEIGHT_HEALTH_BAR = 0.125

    #Physics
    FRICTION_DEFAULT = 320		#The rate at which objects slow while on Terrain TODO
    GRAVITY_DEFAULT = 80		#The rate at which objects accelerate downwards
    MAX_SPEED_DEFAULT = 320		#The max speed an object can travel

    #World generation
    WORLD_DEFAULT_HEIGHT = 64		#The initial height of Terrain in a new World, aka sea level
    WORLD_DEFAULT_HEIGHT_RANGE = 16	#The initial max variation in Terrain height in a new World
    WORLD_DEFAULT_HEIGHT_STEP = 4	#The initial max variation in Terrain height compared to the next Terrain in a new World    
    WORLD_DEFAULT_HEIGHT_WIDTH = 4	#The initial width of Terrain in a new World that is always the default height
    WORLD_DEFAULT_WIDTH = 32		#The initial width of Terrain in a new World

    #World limits
    WORLD_HEIGHT_MAX = 128		#The max height of the world
    WORLD_VIEW_HEIGHT = 7		#The max height to display
    WORLD_VIEW_WIDTH = 10		#The max width to display
    WORLD_WIDTH_MAX = 1024		#The max width of the world

    #Define the constructor
    def __init__(self, name, seedValue):
        #Set World fields
        self.name = name
        self.seedValue = seedValue	#The original seedValue

        #Initialize World fields
        self.ammo = []			#Ammo
        self.effects = []		#Effects
        self.entitys = []		#Entitys

        self.terrain = []		#Viewable Terrain, lazy loaded/pruned, derived from self.terrainTypes, used for bulk updates/draw calls
        self.terrainNodes = {}		#Viewable Terrain, lazy loaded/pruned, derived from self.terrainTypes, used for collision detection
        self.terrainTypes = {}		#Terrain stored as enums, with the shape { posX -> { posY -> Terrain Type } }, ground/sea level having a posY of 0

        self.selectables = []		#Objects that are selectable by the Player, Entitys/Terrain

        #Create the World and ensure the Terrain is visible
        self.createWorld()
        self.ensureTerrainVisible(0, 0)

    #Create a World based on the seedValue
    def createWorld(self):
        #Seed the random number generator
        random.seed(self.seedValue)

        #Set physics values
        self.friction = self.FRICTION_DEFAULT
        self.gravity = self.GRAVITY_DEFAULT
        self.maxSpeed = self.MAX_SPEED_DEFAULT

        #Add Terrain to the left/right of the Player
        for i in range(0, self.WORLD_DEFAULT_WIDTH):
            self.generateTerrain(-i - 1)
            self.generateTerrain(i)

        #Add floating Terrain as a test
        self.terrainTypes[-1][5] = TerrainType.DIRT
        self.terrainTypes[0][5] = TerrainType.DIRT

        #Add an enemy Entity
        self.addEntity(Entity.Entity(50, 0, 0, 0, 0, Team.ENEMY, EntityType.ROBOT))

    #Generate new Terrain at posX
    def generateTerrain(self, posX):
        #Initialize the terrainTypes dict for posX
        self.terrainTypes[posX] = {}

        #print("Generating Terrain for posX: " + str(posX))

        #Get the new Terrain height
        terrainHeight = self.WORLD_DEFAULT_HEIGHT
        #If posX is left of the default area, use the previous left Terrain to calculate the new height
        if posX < -self.WORLD_DEFAULT_HEIGHT_WIDTH:
            previousHeight = self.WORLD_DEFAULT_HEIGHT + max(self.terrainTypes[posX + 1].keys()) + 1
            random.seed(int(self.seedValue * posX))
            terrainHeight = previousHeight + random.randrange(-self.WORLD_DEFAULT_HEIGHT_STEP, self.WORLD_DEFAULT_HEIGHT_STEP + 1)
        #If posX is right of the default area, use the previous right Terrain to calculate the new height
        elif self.WORLD_DEFAULT_HEIGHT_WIDTH < posX:
            previousHeight = self.WORLD_DEFAULT_HEIGHT + max(self.terrainTypes[posX - 1].keys()) + 1
            random.seed(str(self.seedValue * posX))
            terrainHeight = previousHeight + random.randrange(-self.WORLD_DEFAULT_HEIGHT_STEP, self.WORLD_DEFAULT_HEIGHT_STEP + 1)

        #Ensure the new Terrain height is within limits
        if terrainHeight < self.WORLD_DEFAULT_HEIGHT - self.WORLD_DEFAULT_HEIGHT_RANGE:
            terrainHeight = self.WORLD_DEFAULT_HEIGHT - self.WORLD_DEFAULT_HEIGHT_RANGE
        elif terrainHeight > self.WORLD_DEFAULT_HEIGHT + self.WORLD_DEFAULT_HEIGHT_RANGE:
            terrainHeight = self.WORLD_DEFAULT_HEIGHT + self.WORLD_DEFAULT_HEIGHT_RANGE

        #print("\tHeight: " + str(terrainHeight))

        #For the height of the Terrain, add Terrain
        for i in range(-self.WORLD_DEFAULT_HEIGHT, -self.WORLD_DEFAULT_HEIGHT + terrainHeight):
           self.terrainTypes[posX][i] = TerrainType.DIRT

    #Add an Ammo to the World
    def addAmmo(self, node):
        self.ammo.append(node)

    #Add an Effect to the World
    def addEffect(self, node):
        self.effects.append(node)

    #Add an Entity to the World
    def addEntity(self, node):
        self.entitys.append(node)
        self.selectables.append(node)

    #Add an Terrain to the World, note: visible Terrain only
    def addTerrain(self, node):
        self.terrain.append(node)
        self.selectables.append(node)

    #Ensure that only the Terrain that should be visible is
    def ensureTerrainVisible(self, posX, posY):
        #Calculate the max x/y positions for Terrain that should be visible, converting from pixel position
        #Note: y-axis is negative for pixel position
        checkYTop = int(-posY / Terrain.TERRAIN_SIZE) + self.WORLD_VIEW_HEIGHT + 1	#TODO adjustment for drawing from top left
        checkYBottom = int(-posY / Terrain.TERRAIN_SIZE) - self.WORLD_VIEW_HEIGHT
        checkXLeft = int(posX / Terrain.TERRAIN_SIZE) - self.WORLD_VIEW_WIDTH - 1	#TODO adjustment for drawing from top left
        checkXRight = int(posX / Terrain.TERRAIN_SIZE) + self.WORLD_VIEW_WIDTH

        #print("ensureTerrainVisible check: " + str(checkXLeft) + ", " + str(checkYTop) + " to " + str(checkXRight) + ", " + str(checkYBottom))

        #For all Terrain x positions to check
        for x in range(checkXLeft, checkXRight + 1):
            #If the dict for x hasn't be initialized, do so
            if x not in self.terrainNodes.keys():
                self.terrainNodes[x] = {}

            #If x isn't a valid key in self.terrainTypes
            if x not in self.terrainTypes.keys():
                self.generateTerrain(x)

            #If x is a valid key in self.terrainTypes
            if x in self.terrainTypes.keys():
                #For all Terrain y positions to check
                for y in range(checkYBottom, checkYTop + 1):
                    #If the Terrain for y hasn't be loaded, load it
                    if y not in self.terrainNodes[x].keys() and y in self.terrainTypes[x].keys():
                        #print("Loading: " + str(x) + ", " + str(y))
                        self.terrainNodes[x][y] = Terrain.Terrain(x * Terrain.TERRAIN_SIZE, -y * Terrain.TERRAIN_SIZE, self.terrainTypes[x][y])
                        self.addTerrain(self.terrainNodes[x][y])

        #For all Terrain x positions
        for x in list(self.terrainNodes.keys()):
            #If Terrain x position should be pruned, do so
            if x < checkXLeft or checkXRight < x:
                for y in list(self.terrainNodes[x].keys()):
                    self.removeTerrain(self.terrainNodes[x][y])
                    del self.terrainNodes[x][y]
                del self.terrainNodes[x]
            #Otherwise, for all Terrain y positions
            else:
                for y in list(self.terrainNodes[x].keys()):
                    #If Terrain y position should be pruned, do so
                    if y < checkYBottom or checkYTop < y:
                        self.removeTerrain(self.terrainNodes[x][y])
                        del self.terrainNodes[x][y]

        #print("Ensure Done")

    #Run Entity AI
    def entityAI(self, entity, frameDeltaTime):
        target = entity.target

        #If the Entity has no target, find the closest enemy
        if not target:
            target = self.getClosestEntity(entity, None, entity.team)

        #If the entity has a target
        if target:
            #Get its relative positon
            relativePosition = target.position - entity.position

            #Move towards it
            if relativePosition.x < 0:
                self.nodeMove(entity, -entity.speed * frameDeltaTime, 0)
            else:
                self.nodeMove(entity, entity.speed * frameDeltaTime, 0)

            #If the Entity can attack and the target is in range, attack based on attackType
            if entity.canAttack() and relativePosition.getLengthSQ() < entity.attackRangeSQ:
                if entity.attackType is AttackType.MELEE:
                    self.entityAttackMelee(entity)
                elif entity.attackType is AttackType.RANGED:
                    self.entityAttackRanged(entity, target.position.x, target.position.y)
                elif entity.attackType is AttackType.SPELL:
                    self.entityAttackSpell(entity, target.position.x, target.position.y)
                elif entity.attackType is AttackType.SUMMON:
                    self.entityAttackSummon(entity, target.position.x, target.position.y)

            #TODO AI, jump only when required
            #self.entityJump(entity)

    #Have an Entity attack using Melee
    def entityAttackMelee(self, entity):
        #If the Entity can attack using melee
        if entity.attackMelee():
            #Find the closest enemy
            enemy = self.getClosestEntity(entity, entity.meleeRange, entity.team)

            #If the enemy was in range, hit
            if enemy:
                self.entityHit(enemy, entity.meleeDamage)

    #Have an Entity attack using Ranged
    def entityAttackRanged(self, entity, targetX, targetY):
        #If the Entity can attack using ranged
        if entity.attackRanged():
            #Because position tracks the top left corner of the object the following calculatings are required
            posX = entity.position.x + entity.widthHalf - Ammo.AMMO_SIZE_HALF
            posY = entity.position.y + entity.heightHalf - Ammo.AMMO_SIZE_HALF
            dirX = targetX - entity.position.x - entity.widthHalf
            dirY = targetY - entity.position.y - entity.heightHalf

            #Create the Ammo
            self.addAmmo(Ammo.Ammo(posX, posY, dirX, dirY, entity.team, AmmoType.RANGED, entity.rangedDamage, entity.rangedRange, entity.rangedSpeed))

    #Have an Entity attack using Spell
    def entityAttackSpell(self, entity, targetX, targetY):
        #If the Entity can attack using a spell
        if entity.attackSpell():
            #Because position tracks the top left corner of the object the following calculatings are required
            posX = entity.position.x + entity.widthHalf - Ammo.AMMO_SIZE_HALF
            posY = entity.position.y + entity.heightHalf - Ammo.AMMO_SIZE_HALF
            dirX = targetX - entity.position.x - entity.widthHalf
            dirY = targetY - entity.position.y - entity.heightHalf

            #Create the Ammo
            self.addAmmo(Ammo.Ammo(posX, posY, dirX, dirY, entity.team, AmmoType.SPELL, entity.spellDamage, entity.spellRange, entity.spellSpeed))

    #Have an Entity Attack using Summon
    def entityAttackSummon(self, entity, targetX, targetY):
        #If the Entity can attack using a spell
        if entity.attackSpell():
            #Because position tracks the top left corner of the object the following calculatings are required
            posX = targetX - entity.widthHalf
            posY = targetY - entity.heightHalf

            #Add an Effect/Entity
            self.addEffect(Effect.ExplosionVertical(entity.width, entity.height, posX, posY))
            self.addEntity(Entity.Entity(posX, posY, 0, 0, 0, entity.team, EntityType.ROBOT))

    #Apply Gravity to an Entity depending on what if any Terrain it is on
    def entityGravity(self, entity, frameDeltaTime):
        #Get the Terrain the Entity is on if any
        onTerrain = self.isEntityOnTerrain(entity)

        #If the Entity is on Terrain, ensure the Entitys vertical position and direction
        if onTerrain:
            entity.position.y = onTerrain.y - entity.height
            entity.direction.y = 0
        #Otherwise, apply gravity to the Entity
        else:
            entity.accelerate(0, self.gravity * frameDeltaTime)
            entity.ensureMaxSpeed(self.maxSpeed)

    #Apply Damage to an Entity
    def entityHit(self, entity, damage):
        entity.damage(damage)

        #If the Entity already has a Health Bar Effect, update its width
        if entity.healthBar:
            entity.healthBar.setWidth(int(entity.width * entity.getHealthPercentage()))
            entity.healthBar.resetTimeLeft()
        #Otherwise, add a Health Bar Effect
        else:
            self.addEffect(Effect.HealthBar(int(entity.width * entity.getHealthPercentage()), int(entity.height * self.HEIGHT_HEALTH_BAR), entity.position.x, entity.position.y))
            self.effects[-1].entity = entity
            self.effects[-1].position = entity.position
            entity.healthBar = self.effects[-1]

    #Have an Entity Jump
    def entityJump(self, entity):
        #If the Entity is on Terrain, jump
        if self.isEntityOnTerrain(entity):
            self.nodeMove(entity, entity.direction.x, -entity.getJumpHeight())
            entity.direction.y = 0
            #entity.jump()   #TODO remove?

    #Get the closest Entity optionally with range and not belonging to the same team
    def getClosestEntity(self, entity, range, team):
        closestDistanceSQ = None
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
    def getClosestNode(self, position, range):
        closestDistanceSQ = None
        closestNode = None

        #For all selectable Nodes, find the closest
        for node in self.selectables:
            if closestNode is None or closestDistanceSQ > position.getLengthTo(node.getCentre()) - node.widthHalf:
               if range is None or range >= position.getLengthTo(node.getCentre()) - node.widthHalf:
                   closestNode = node
                   closestDistanceSQ = position.getLengthTo(node.getCentre()) - node.widthHalf

        return closestNode

    #Test whether the Entity is on Terrain, returns the Terrain if it is, else None
    def isEntityOnTerrain(self, entity):
        #Calculate facts about the Entity position used for detecting whether the Entity is on Terrain, note: reduced width and entityYBottom + 1 so can check for collision
        #Note: y-axis is negative for pixel position
        #TODO magic values
        entityYTop = -entity.position.y - entity.height * 0.5
        entityYBottom = -entity.position.y - entity.height - 1
        entityXLeft = entity.position.x + entity.width * 0.25
        entityXRight = entity.position.x + entity.width * 0.75

        #print("isEntityOnTerrain entity: " + str(entityXLeft) + ", " + str(entityYTop) + " to " + str(entityXRight) + ", " + str(entityYBottom))

        #Calculate the max x/y positions for Terrain around Entity to check if Entity on top of, converting from pixel position
        checkYTop = int(entityYTop / Terrain.TERRAIN_SIZE) + 1
        checkYBottom = int(entityYBottom / Terrain.TERRAIN_SIZE) - 1
        checkXLeft = int(entityXLeft / Terrain.TERRAIN_SIZE) - 1
        checkXRight = int(entityXRight / Terrain.TERRAIN_SIZE) + 1

        #print("isEntityOnTerrain check: " + str(checkXLeft) + ", " + str(checkYTop) + " to " + str(checkXRight) + ", " + str(checkYBottom))

        #For all Terrain x positions to check
        for x in range(checkXLeft, checkXRight + 1):
            xLeft, xRight = x * Terrain.TERRAIN_SIZE, (x + 1) * Terrain.TERRAIN_SIZE
            #If x is a valid key in self.terrainTypes and x is between the left and right Terrain x values
            if x in self.terrainTypes.keys() and xLeft < entityXRight and xRight > entityXLeft:
                #For all Terrain y positions to check
                for y in range(checkYBottom, checkYTop + 1):
                    #If y is a valid key in self.terrainTypes
                    if y in self.terrainTypes[x].keys():
                        yTop, yBottom = y * Terrain.TERRAIN_SIZE, (y - 1) * Terrain.TERRAIN_SIZE
                        #If y is between the bottom and top Terrain y values, return the Terrains position
                        if yTop > entityYBottom and yBottom < entityYTop:
                            return Vector2f(x * Terrain.TERRAIN_SIZE, -y * Terrain.TERRAIN_SIZE)

        return None

    #Move a Node
    def nodeMove(self, node, dirX, dirY):
        #Calculate facts about the new Node position used for detecting whether the Node will collide with something
        #Note: y-axis is negative for pixel position
        nodeYTop = -node.position.y - dirY
        nodeYBottom = -node.position.y - node.height - dirY
        nodeXLeft = node.position.x + dirX
        nodeXRight = node.position.x + node.width + dirX

        #print("nodeMove node: " + str(nodeXLeft) + ", " + str(nodeYTop) + " to " + str(nodeXRight) + ", " + str(nodeYBottom))

        #Calculate the max x/y positions for Terrain around Node to check if Node will collide width, converting from pixel position
        checkYTop = int(nodeYTop / Terrain.TERRAIN_SIZE) + 1
        checkYBottom = int(nodeYBottom / Terrain.TERRAIN_SIZE) - 1
        checkXLeft = int(nodeXLeft / Terrain.TERRAIN_SIZE) - 1
        checkXRight = int(nodeXLeft / Terrain.TERRAIN_SIZE) + 1

        #print("nodeMove check: " + str(checkXLeft) + ", " + str(checkYTop) + " to " + str(checkXRight) + ", " + str(checkYBottom))

        collision = False

        #For all Terrain x positions to check
        for x in range(checkXLeft, checkXRight + 1):
            xLeft, xRight = x * Terrain.TERRAIN_SIZE, (x + 1) * Terrain.TERRAIN_SIZE
            #If x is a valid key in self.terrainTypes and x is between the left and right Terrain x values
            if x in self.terrainTypes.keys() and xLeft < nodeXRight and xRight > nodeXLeft:
                #For all Terrain y positions to check
                for y in range(checkYBottom, checkYTop + 1):
                    #If y is a valid key in self.terrainTypes
                    if y in self.terrainTypes[x].keys():
                        yTop, yBottom = y * Terrain.TERRAIN_SIZE, (y - 1) * Terrain.TERRAIN_SIZE
                        #if node.nodeType == NodeType.AMMO:
                            #print("\tAmmo check: " + str(x) + "," + str(y))
                            #print("\t" + str(xLeft) +" < "+ str(nodeXRight) +" and "+ str(xRight) +" > "+ str(nodeXLeft))
                            #print("\t" + str(yTop) +" > "+ str(nodeYBottom) +" and "+ str(yBottom) +" < "+ str(nodeYTop))
                        #If y is between the bottom and top Terrain y values and collision is False
                        if collision is False and yTop > nodeYBottom and yBottom < nodeYTop:
                            collision = True

                            #print("Hit: " + str(x) + ", " + str(y))
                            #print("\t" + str(xLeft) +" < "+ str(nodeXRight) +" and "+ str(xRight) +" > "+ str(nodeXLeft))
                            #print("\t" + str(yTop) +" > "+ str(nodeYBottom) +" and "+ str(yBottom) +" < "+ str(nodeYTop))
                            #print("DirX: " + str(dirX))

                            #Depending on whether the Node is moving left/right/up/down and the collision happens, set move values and direction
                            if dirX < 0 and xRight <= node.position.x:
                                dirX = xRight - node.position.x
                                if dirX > 0:
                                    dirX = 0
                                node.direction.x = 0
                                #print("Hit1: " + str(dirX))
                            elif dirX > 0 and xLeft >= node.position.x + node.width:
                                dirX = xLeft - node.position.x - node.width
                                if dirX < 0:
                                    dirX = 0
                                node.direction.x = 0
                                #print("Hit2")
                            if -dirY > 0 and yBottom >= -node.position.y:
                                dirY = yBottom - -node.position.y
                                dirY = -dirY
                                if -dirY < 0:
                                    dirY = 0
                                node.direction.y = 0
                                print("Hit3: " + str(dirY))
                            elif -dirY < 0 and yTop <= -node.position.y - node.height:
                                dirY = yTop - node.position.y + node.height
                                dirY = -dirY
                                if -dirY > 0:
                                    dirY = 0
                                node.direction.y = 0
                                print("Hit4: " + str(dirY))

        #If Node is an ammo
        if node.nodeType == NodeType.AMMO:
            #If no collision has happened, check all Entitys for a collision
            if collision is False:
                for entity in self.entitys:
                    xLeft, xRight = entity.position.x, entity.position.x + entity.width
                    yTop, yBottom = -entity.position.y, -entity.position.y - entity.height
                    if node.team is not entity.team and xLeft < nodeXRight and xRight > nodeXLeft and yTop > nodeYBottom and yBottom < nodeYTop:
                        self.entityHit(entity, node.damage)
                        collision = True

            #If a collision has happened
            if collision is True:
                #Create an Effect/Sound for the explosion
                self.addEffect(Effect.Explosion(node.width, node.height, nodeXLeft, -nodeYTop))
                #TODO add sound

                #Remove the Ammo and return
                self.removeAmmo(node)
                return

        #If dirX or dirY are non 0, move the Node
        if dirX != 0 or dirY != 0:
            node.move(dirX, dirY)

    #Remove an Ammo from the World
    def removeAmmo(self, node):
        self.ammo.remove(node)

    #Remove an Effect from the World
    def removeEffect(self, node):
        self.effects.remove(node)

    #Remove an Entity from the World
    def removeEntity(self, node):
        self.entitys.remove(node)
        self.selectables.remove(node)

    #Remove an Terrain from the World
    def removeTerrain(self, node):
        self.terrain.remove(node)
        self.selectables.remove(node)

    #Update the World, apply Gravity, Direction etc.
    def update(self, player, frameDeltaTime):
        #For all Entitys
        for node in self.entitys:
            #If the Entity has expired, remove it
            if node.update(frameDeltaTime):
                #If the Entity has an Effect, make sure the Effect doesn't reference the Entity
                if node.healthBar:
                    node.healthBar = None
                self.removeEntity(node)
                continue

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
                self.removeAmmo(node)
                continue

            #If the Ammo type is Ranged, apply Gravity
            if node.type is AmmoType.RANGED:
                self.entityGravity(node, frameDeltaTime)

            #Apply Direction
            self.nodeMove(node, node.direction.x * frameDeltaTime, node.direction.y * frameDeltaTime)

        #For all Effects
        for node in self.effects:
            #If the Effect has expired, remove it
            if node.update(frameDeltaTime):
                #If the Effect has an Entity, make sure the Entity doesn't reference the Effect
                if node.entity:
                    node.entity.healthBar = None
                self.removeEffect(node)
                continue

            #If the Effect is a Health Bar and references a Entity, update its width
            if node.type is EffectType.HEALTH_BAR and node.entity:
                node.setWidth(int(node.entity.width * node.entity.getHealthPercentage()))

            #Apply Direction, note: no collision checking
            node.move(node.direction.x * frameDeltaTime, node.direction.y * frameDeltaTime)

        #Ensure Terrain visible
        self.ensureTerrainVisible(player.position.x, player.position.y)

        #For all Terrain, Update
        for node in self.terrain:
            node.update(frameDeltaTime)



