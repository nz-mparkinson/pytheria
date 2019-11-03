#!/usr/bin/python

#Import libraries
import random

from ammo import *
from effect import *
from entity import *
from terrain import *

#Define a class for World, which manages all Nodes in a locale
class World:
    FRICTION_DEFAULT = 50           #TODO implement
    GRAVITY_DEFAULT = 200
    HEIGHT_HEALTH_BAR = 0.125
    MAX_SPEED_DEFAULT = 400
    WORLD_HEIGHT_DEFAULT = 16
    WORLD_HEIGHT_DEFAULT_WIDTH = 4
    WORLD_HEIGHT_DIFFERENCE_MAX = 8
    WORLD_HEIGHT_STEP_MAX = 2
    WORLD_WIDTH = 32

    #Define the constructor
    def __init__(self, name, seedValue):
        self.name = name
        self.seedValue = seedValue

        self.ammo = []
        self.effects = []
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
                self.addTerrain(Terrain.Terrain(i * Terrain.TERRAIN_SIZE, -j * Terrain.TERRAIN_SIZE, TerrainType.DIRT))

        #Seed the random number generator
        random.seed(self.seedValue)

        #Add Terrain with random heights to the left/right of the Player
        terrainHeightLeft, terrainHeightRight = 0, 0
        for i in range(self.WORLD_HEIGHT_DEFAULT_WIDTH, self.WORLD_WIDTH):
            #Get the next Terrain height to the left
            terrainHeightLeft = terrainHeightLeft + random.randrange(-self.WORLD_HEIGHT_STEP_MAX, self.WORLD_HEIGHT_STEP_MAX+1)
            if terrainHeightLeft < -self.WORLD_HEIGHT_DIFFERENCE_MAX:
                terrainHeightLeft = -self.WORLD_HEIGHT_DIFFERENCE_MAX
            elif terrainHeightLeft > self.WORLD_HEIGHT_DIFFERENCE_MAX:
                terrainHeightLeft = self.WORLD_HEIGHT_DIFFERENCE_MAX

            #Add Terrain to the left
            for j in range(-self.WORLD_HEIGHT_DEFAULT, terrainHeightLeft):
                self.addTerrain(Terrain.Terrain(-i * Terrain.TERRAIN_SIZE, -j * Terrain.TERRAIN_SIZE, TerrainType.DIRT))

            #Get the next Terrain height to the right
            terrainHeightRight = terrainHeightLeft + random.randrange(-self.WORLD_HEIGHT_STEP_MAX, self.WORLD_HEIGHT_STEP_MAX+1)
            if terrainHeightRight < -self.WORLD_HEIGHT_DIFFERENCE_MAX:
                terrainHeightRight = -self.WORLD_HEIGHT_DIFFERENCE_MAX
            elif terrainHeightRight > self.WORLD_HEIGHT_DIFFERENCE_MAX:
                terrainHeightRight = self.WORLD_HEIGHT_DIFFERENCE_MAX

            #Add Terrain to the right
            for j in range(-self.WORLD_HEIGHT_DEFAULT, terrainHeightRight):
                self.addTerrain(Terrain.Terrain(i * Terrain.TERRAIN_SIZE, -j * Terrain.TERRAIN_SIZE, TerrainType.DIRT))

        #Add an enemy Entity
        self.addEntity(Entity.Entity(50, 0, 0, 0, 0, Team.ENEMY, EntityType.ROBOT))

    #Add an Ammo to the World
    def addAmmo(self, node):
        self.ammo.append(node)

    #Add an Effect to the World
    def addEffect(self, node):
        self.effects.append(node)

    #Add an Entity to the World
    def addEntity(self, node):
        self.entitys.append(node)
        self.collidables.append(node)
        self.selectables.append(node)

    #Add an Terrain to the World
    def addTerrain(self, node):
        self.terrain.append(node)
        self.collidables.append(node)
        self.selectables.append(node)

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
        onTerrain = None
        onTerrain = self.isEntityOnTerrain(entity)

        #If the Entity is on Terrain, ensure the Entitys vertical position and direction
        if onTerrain:
            entity.position.y = onTerrain.position.y - entity.height
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
        for collidable in self.collidables:
            #Skip if the Node and Collidable are on the same team
            if collidable.team == node.team:
                pass
            #Skip if the Node and Collidable are both Entitys
            elif collidable.nodeType == NodeType.ENTITY and node.nodeType == NodeType.ENTITY:
                pass
            #Skip if the Node is too far left
            elif collidable.position.x + collidable.width <= nodeXLeft:
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
            #If the Node is an Ammo
            elif node.nodeType == NodeType.AMMO:
                #Move the Ammo
                node.move(x, y)

                #Create an Effect/Sound for the explosion
                self.addEffect(Effect.Explosion(node.width, node.height, node.position.x, node.position.y))
                #TODO add sound

                #If the Collidable is an Entity, damage the Entity
                if collidable.nodeType == NodeType.ENTITY:
                    self.entityHit(collidable, node.damage)

                #Remove the Ammo and return
                self.removeAmmo(node)
                return
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

    #Remove an Effect from the World
    def removeEffect(self, node):
        self.effects.remove(node)

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

        #For all Terrain, Update
        for node in self.terrain:
            node.update(frameDeltaTime)



