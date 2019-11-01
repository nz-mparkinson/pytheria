#!/usr/bin/python


#Import libraries
import pygame
from pygame.locals import *

from world import *

#TODO
# _ for private variables

#Define a class for the Game
class Game:
    #Define the constructor
    def __init__(self, width, height, maxFPS):
        self.height = height
        self.maxFPS = maxFPS
        self.width = width

        self.frameDeltaTime = 0
        self.playTime = 0.0
        self.running = False
        self.size = width, height

        self.background = None
        self.clock = None
        self.font = None
        self.player = None
        self.screen = None
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

        self.running = True

    #Define a function for event handling
    def on_event(self, event):
        #If the event is quit, set running to False
        if event.type == pygame.QUIT:
            self.running = False
        #If the event is a key down, get all keys and react accordingly
        elif event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()

            #If escape key pressed, exit the Game
            if keys[pygame.K_ESCAPE]:
                self.running = False
            #If left key pressed, move the player left
            if keys[pygame.K_LEFT]:
                self.world.entityMove(self.player, -5, 0)
            #If right key pressed, move the player right
            elif keys[pygame.K_RIGHT]:
                self.world.entityMove(self.player, 5, 0)
            #If up key pressed, move the player up
            if keys[pygame.K_UP]:
                self.world.entityMove(self.player, 0, -5)
            #If down key pressed, move the player down
            elif keys[pygame.K_DOWN]:
                self.world.entityMove(self.player, 0, 5)
            #TODO sometimes can't jump
            #If space key pressed and the Player is on Terrain, move the player up
            if keys[pygame.K_SPACE] and self.world.isEntityOnTerrain(self.player):
                self.world.entityMove(self.player, 0, -25)
                self.player.state = EntityState.JUMPING

    #Define a function for Game logic
    def on_loop(self):
        #Update the World, apply Gravity, Direction etc.
        self.world.update(self.player, self.frameDeltaTime)

    #Define a function for rendering the Game state
    def on_render(self):
        #Clear the screen
        self.screen.blit(self.background, (0, 0))

        #Calculate the Player position relative to the centre of the screen
        xPos, yPos = self.player.position.x - self.width // 2, self.player.position.y - self.height // 2

        #Draw all Terrain
        for node in self.world.terrain:
            self.screen.blit(node.image, (node.position.x - xPos, node.position.y - yPos))
        #Draw all Entitys
        for node in self.world.entitys:
            self.screen.blit(node.image, (node.position.x - xPos, node.position.y - yPos))
        #Draw all Ammo
        for node in self.world.ammo:
            self.screen.blit(node.image, (node.position.x - xPos, node.position.y - yPos))

        #Draw the Player in the centre of the screen
        self.screen.blit(self.player.image, (self.width // 2, self.height // 2))

        #Draw the FPS
        fps = self.font.render("FPS: {:6.3}{}TIME: {:6.3}".format(self.clock.get_fps(), " "*5, self.playTime), True, (0, 255, 0))
        self.screen.blit(fps, (0, 0))

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
        self.player = Entity(Entity.WIDTH_DEFAULT, Entity.HEIGHT_DEFAULT, 0, 0, 0, 0, 0, "../resources/mine/circle.png", 0)
        self.world.entitys.append(self.player)

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

            #Render the Game state
            self.on_render()

        #When the Game stops running, cleanup
        self.on_cleanup()



#If this script is being run, start the game
if __name__ == "__main__":
    game = Game(640, 400, 60)
    game.on_execute()



