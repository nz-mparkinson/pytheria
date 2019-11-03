#!/usr/bin/python




#Import libraries
import pygame
from pygame.locals import *

from gui import *
from world import *

#TODO
# _ for private variables
# positions are top left, change to be centre and only have draw calls use function getting top left? use node.image.position as top left?

#Define a class for the Game
class Game:
    SELECT_RANGE = 4

    #Define the constructor
    def __init__(self, width, height, maxFPS):

        #Set Game fields
        self.height = height
        self.heightHalf = height // 2
        self.maxFPS = maxFPS
        self.width = width
        self.widthHalf = width // 2

        #Initialize Game fields
        self.frameDeltaTime = 0
        self.playTime = 0.0
        self.running = False
        self.size = width, height

        #Initialize Game pointers
        self.background = None
        self.clock = None
        self.font = None
        self.gui = None
        self.keysPrevious = None
        self.player = None
        self.reticle = None
        self.screen = None
        self.selectedNode = None
        self.world = None

    #Define a function for initializing the Game
    def on_init(self):
        #Initialize PyGame
        pygame.init()
        pygame.key.set_repeat(True)
        
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('mono', 20, bold=True)
        self.screen = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.background = pygame.Surface(self.screen.get_size()).convert()
        self.reticle = Effect.Reticle(self.SELECT_RANGE, self.SELECT_RANGE, 0, 0)
        self.keysPrevious = pygame.key.get_pressed()

        self.gui = GUI(self.width, self.height)

        self.running = True

    #Define a function for event handling
    def on_event(self, event):
        #If the event is quit, set running to False
        if event.type == pygame.QUIT:
            self.running = False
        #If the event is a key down, get all keys and react accordingly
        if event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()

            #If escape key pressed, exit the Game
            if keys[pygame.K_ESCAPE] and not self.keysPrevious[pygame.K_ESCAPE]:
                self.running = False

            #If left key down, move the player left
            if keys[pygame.K_LEFT]:
                self.world.nodeMove(self.player, -5, 0)
            #If right key down, move the player right
            elif keys[pygame.K_RIGHT]:
                self.world.nodeMove(self.player, 5, 0)
            #If up key down, move the player up
            if keys[pygame.K_UP]:
                self.world.nodeMove(self.player, 0, -5)
            #If down key down, move the player down
            elif keys[pygame.K_DOWN]:
                self.world.nodeMove(self.player, 0, 5)
            #If space key down, move the player up
            if keys[pygame.K_SPACE]:
                self.world.entityJump(self.player)

            #If j key pressed, toggle AttackType backward
            if keys[pygame.K_j] and not self.keysPrevious[pygame.K_j]:
                self.player.toggleAttackType(False)
            #If k key pressed, toggle AttackType forward
            if keys[pygame.K_k] and not self.keysPrevious[pygame.K_k]:
                self.player.toggleAttackType(True)

        #If the event is a mouse press, get the mouse position and all mouse buttons and react accordingly
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            pressed1, pressed2, pressed3 = pygame.mouse.get_pressed()

            #Calculate the mouse position in the world
            posX = self.player.position.x + pos[0] - self.widthHalf
            posY = self.player.position.y + pos[1] - self.heightHalf

            #If the left mouse pressed, attack
            if pressed1:
                if self.player.attackType == AttackType.MELEE:
                    self.world.entityAttackMelee(self.player)
                elif self.player.attackType == AttackType.RANGED:
                    self.world.entityAttackRanged(self.player, posX, posY)
                elif self.player.attackType == AttackType.SPELL:
                    self.world.entityAttackSpell(self.player, posX, posY)
                elif self.player.attackType == AttackType.SUMMON:
                    self.world.entityAttackSummon(self.player, posX, posY)
            #If the middle mouse pressed
            if pressed2:
                #TODO
                pass
            #If the right mouse pressed, interact/mine
            if pressed3:
                #TODO
                pass

            #If the mouse wheel was moved up, toggle AttackType backward
            if event.button == 4:
                self.player.toggleAttackType(False)
            #If the mouse wheel was moved down, toggle AttackType forward
            elif event.button == 5:
                self.player.toggleAttackType(True)
        #If the event is a mouse move, select the Node near the mouse
        if event.type == pygame.MOUSEMOTION:
            pos = pygame.mouse.get_pos()

            #Calculate the mouse position in the world
            posX = self.player.position.x + pos[0] - self.widthHalf
            posY = self.player.position.y + pos[1] - self.heightHalf

            #Get the Node near the mouse
            temp = self.world.getClosestNode(Vector2f(posX, posY), self.SELECT_RANGE)

            #Set the Reticle size
            if temp and temp is not self.selectedNode:
                self.reticle.setSize(temp.width, temp.height)
                self.reticle.setColour(Effect.COLOUR_RETICLE[0], Effect.COLOUR_RETICLE[1], Effect.COLOUR_RETICLE[2])

            self.selectedNode = temp

        #Remember the key state for the next call
        self.keysPrevious = pygame.key.get_pressed()

    #Define a function for Game logic
    def on_loop(self):
        #Update the World, apply Gravity, Direction etc.
        self.world.update(self.player, self.frameDeltaTime)

    #Define a function for rendering the Game state
    def on_render(self):
        #Clear the screen
        self.screen.blit(self.background, (0, 0))

        #Calculate the Player position relative to the centre of the screen
        xPos, yPos = self.player.position.x - self.widthHalf, self.player.position.y - self.heightHalf

        #Draw all Terrain
        for node in self.world.terrain:
            self.screen.blit(node.image, (node.position.x - xPos, node.position.y - yPos))
        #Draw all Entitys
        for node in self.world.entitys:
            if node is not self.player:
                self.screen.blit(node.image, (node.position.x - xPos, node.position.y - yPos))
        #Draw the Player in the centre of the screen
        self.screen.blit(self.player.image, (self.widthHalf, self.heightHalf))
        #Draw all Ammo
        for node in self.world.ammo:
            self.screen.blit(node.image, (node.position.x - xPos, node.position.y - yPos))
        #Draw all Effects
        for node in self.world.effects:
            self.screen.blit(node.image, (node.position.x - xPos, node.position.y - yPos))

        #Draw the FPS
        fps = self.font.render("FPS: {:6.3}{}TIME: {:6.3}".format(self.clock.get_fps(), " "*5, self.playTime), True, (0, 255, 0))
        self.screen.blit(fps, (0, 0))

        #If a Node is selected, draw its name
        if self.selectedNode:
            #TODO hover for target info
            selectedText = self.font.render("FPS: {:6.3}{}TIME: {:6.3}".format(self.clock.get_fps(), " "*5, self.playTime), True, (0, 255, 0))
            self.screen.blit(fps, (self.width - selectedText.get_width(), self.height - selectedText.get_height()))
            self.screen.blit(self.reticle.image, (self.selectedNode.position.x - xPos, self.selectedNode.position.y - yPos))

        #Draw the GUI Nodes
        for node in self.gui.nodes:
            self.screen.blit(node.image, (node.position.x, node.position.y))

        #Update the screen
        pygame.display.flip()

    #Define a function for cleaning up after the Game stops
    def on_cleanup(self):
        pygame.quit()

    #Define
    def on_execute(self):
        #Initialize the Game, if it fails, set running to False
        if self.on_init() == False:
            self.running = False

        #Create the World
        self.world = World("Test", 11)

        #Create the Player and add it to the World
        self.player = Entity.Entity(Entity.WIDTH_DEFAULT, Entity.HEIGHT_DEFAULT, 0, 0, 0, 0, 0, EntityType.IMMORTAL, 0)
        self.player.attackType = AttackType.SPELL
        self.player.spellDamage = 5
        self.player.spellRateOfFire = 0.05
        self.world.addEntity(self.player)

        #While the Game is running
        while(self.running):
            #Get the new frameDeltaTime and update playTime
            self.frameDeltaTime = self.clock.tick(self.maxFPS) / 1000.0
            self.playTime += self.frameDeltaTime

            #Process all events
            for event in pygame.event.get():
                self.on_event(event)

            #Game logic
            self.on_loop()

            #Update the GUI
            self.gui.update(self.player, self.frameDeltaTime)

            #Render the Game state
            self.on_render()

        #When the Game stops running, cleanup
        self.on_cleanup()



#If this script is being run, start the game
if __name__ == "__main__":
    game = Game(640, 400, 60)
    game.on_execute()



