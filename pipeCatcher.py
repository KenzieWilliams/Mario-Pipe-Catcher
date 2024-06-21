import pygame
from pygame.locals import *
import math
import random
from pgzhelper import *
import time

x = 150
y = 80
import os
os.environ['SDL_VIDEO_WINDOW_POS'] = f'{x},{y}'

import pgzrun

pygame.init()

#set up game variables
score = 0
highScore = 0
timeInterval = 2.5
objVel = 2.5
pipeFreq = 4
gFreq = 1
lost = True
game = False
called = 0
dist = 110
i = 0

#set up lists for active actors
pipeList = []
caughtPipeList = []
goombaList = []

#initialize the window and main character actor
win = pygame.display.set_mode((1536,864))
marioW = Actor('mariowalking.png')
marioW.x = 400
marioW.y = 530
marioW.lives = 3

#create the ground actor
ground = Actor('ground.png')
ground.y = 675

#create all the heart actors (active heart & lost heart)
h1 = Actor('heart.png')
heart2 = Actor('heart.png')
heart3 = Actor('heart.png')
h2 = heart2
h3 = heart3
bw_heart2 = Actor('bwheart.png')
bw_heart3 = Actor('bwheart.png')
h1.x = 590
heart2.x = 650
heart3.x = 710
h1.y = 35
heart2.y = h1.y
heart3.y = h1.y
bw_heart2.x = heart2.x
bw_heart3.x = heart3.x
bw_heart2.y = h1.y
bw_heart3.y = h1.y

#represents the top object on the stack
topObj = marioW

#play lobby music file
music.play('lobby_music')

#every frame
def draw():
    if (game):
        if (not lost):
            #while playing the game, draw all characters, background, & active sprite
            screen.clear()
            screen.blit("skybg.png", (0,0))
            ground.draw()
            marioW.draw()
            for pipe in pipeList:
                pipe.draw()
            for goom in goombaList:
                goom.draw()
            #display the current score, high score, and lives left
            screen.draw.text('Current Score: ' + str(score), (20,20), color = 'lightgrey', fontsize = 40)
            screen.draw.text('High Score: ' + str(highScore), (20,65), color = 'lightgrey', fontsize = 40)
            h1.draw()
            h2.draw()
            h3.draw()
        else: #while on the game screen but lost
            screen.draw.text('You Lost!', (300,180), color = 'red', fontsize = 60)
            screen.draw.text('Final Score: ' + str(score), (260,230), color = 'red', fontsize = 60)
            screen.draw.text('Returning to Home', (200,280), color = 'red', fontsize = 60)
            screen.draw.text('Screen in 3 seconds', (190,330), color = 'red', fontsize = 60)
            
            
    else: #draws the welcome/instruction screen
        screen.clear()
        screen.blit("skybg.png", (0,0))
        screen.draw.text('WELCOME To Pipe Catcher!!', (100,160), color = 'red', fontsize = 60)
        screen.draw.text('Current High Score: ' + str(highScore), (250,225), color = 'red', fontsize = 40)
        screen.draw.text('In this game, you use A & D to help Mario move and catch pipes.', (130,280), color = 'red', fontsize = 25)
        screen.draw.text('Be careful though. If the pipe stack is not straight,', (180,310), color = 'red', fontsize = 25)
        screen.draw.text('the top pipe may not be able to catch all other falling pipes.', (145,340), color = 'red', fontsize = 25)
        screen.draw.text('Press P on the keyboard to play!', (180,380), color = 'red', fontsize = 40)
            
#a practice statement used in the class: currently does nothing
def on_mouse_down():
    pass

#randomly makes either a pipe or a goomba -- increases chances of a goomba as the game goes on
def makeObj():
    global called
    diffFactor = max(10-score,3)
    choice = random.randint(1,diffFactor)
    if choice == 1:
        if called > 2:
            goombaFall()
    else:
        pipeFall()
        called += 1

#creates a falling goomba actor
def goombaFall():
    global lost
    if (not lost):
        goom = Actor('goomba.png')
        goom.x = random.randint(20,760)
        goom.y = -10
        goombaList.append(goom)
        goom.vel = min(max(objVel,objVel+(score/10)),8)

#creates a falling pipe actor
def pipeFall():
    global lost
    if (game and not lost):
        col = random.randint(1,3)
        if col == 1:
            pipe = Actor('greenpipe.png')
        elif col == 2:
            pipe = Actor('pinkpipe.png')
        else:
            pipe = Actor('yellowpipe.png')
        pipe.x = random.randint(20,760)
        pipe.y = -10
        pipeList.append(pipe)
        pipe.vel = min(max(objVel,objVel+(score/10)),8)
        pipe.counted = False

#controls responses to user keyboard input
def on_key_down(key):
    global lost
    global game
    if (not game):
        #if not already playing and the player presses 'p', start the game
        if key == keys.P:
                music.fadeout(.8)
                game = True
                lost = False
                music.play('bg_game_music')
                music.set_volume(.8)
    if (not lost):
        #as long as the game has not been lost, move left or right using 'a' and 'd' keys respectively
        if key == keys.D:
            xChange = marioW.x - min(marioW.x+80,760)
            marioW.x -= xChange
            for pipe in caughtPipeList:
                pipe.x -= xChange
        if key == keys.A:
            xChange = marioW.x-max(marioW.x-80,40)
            marioW.x -= xChange
            for pipe in caughtPipeList:
                pipe.x -= xChange
            
#course of action when the player has lost the game
def loseGame():
    global game
    global score
    global objVel
    global dist
    global i
    global called
    global topObj
    global h3
    global h2
    #fade out game music
    music.fadeout(.8)
    music.stop()
    #wait 3 seconds
    time.sleep(3)
    #play lobby music
    music.play('lobby_music')
    #reset global game variables to their original values
    game = False
    caughtPipeList.clear()
    pipeList.clear()
    goombaList.clear()
    score = 0
    objVel = 2.5
    dist = 110
    marioW.x = 400
    marioW.y = 530
    ground.y = 675
    marioW.lives = 3
    i = 0
    called = 0
    topObj = marioW
    h2 = heart2
    h3 = heart3
        

def update():
    global highScore
    global lost
    global score
    global topObj
    global dist
    global i
    global h3
    global h2
    #if all hearts lost, run the lose game method
    if i == 1:
        loseGame()
    if (game and not lost):
        for pipe in caughtPipeList:
            #check if each caught pipe is still on the screen and, if not, destroy it
            if pipe.y>670:
                caughtPipeList.remove(pipe)
                pipeList.remove(pipe)
        for pipe in pipeList:
            #move each pipe down each frame
            pipe.y += pipe.vel
            if pipe.y > 740:
                #check if each uncaught pipe is still on the screen and, if not, destroy it and lose a life
                pipeList.remove(pipe)
                marioW.lives -= 1
                if marioW.lives == 2:
                    h3 = bw_heart3
                    sounds.lose_heart_sound.play()
                if marioW.lives == 1:
                    h2 = bw_heart2
                    sounds.lose_heart_sound.play()
                if marioW.lives == 0:
                    i = 1
                    sounds.lose_game_sound.play()
                    lost = True
            if pipe.x > topObj.x - 90 and pipe.x < topObj.x + 100:
                #if a pipe is caught by the top object, add it to the list of caught pipes
                if pipe.y + dist <= topObj.y + 3.5 and pipe.y + dist >= topObj.y - 3.5:
                    if (not pipe.counted):
                        score += 1
                        highScore = max(highScore, score)
                        pipe.y = topObj.y-dist
                        pipe.vel = 0
                        pipe.counted = True
                        caughtPipeList.append(pipe)
                        topObj = pipe
                        dist = 90
                        if score > 1:
                            marioW.y += 90
                            ground.y += 90
                            for pipe2 in caughtPipeList:
                                pipe2.y += 90
        for goom in goombaList:
            #move each goomba down the screen
            goom.y += goom.vel
            if goom.x > topObj.x - 50 and goom.x < topObj.x + 100:
                if goom.y + dist <= topObj.y + 3.5 and goom.y + dist >= topObj.y - 3.5:
                    #if goomba hits the top of the stack, remove a life and 3 points
                    score -= 3
                    marioW.lives -= 1
                    if marioW.lives == 2:
                        h3 = bw_heart3
                        sounds.lose_heart_sound.play()
                    if marioW.lives == 1:
                        h2 = bw_heart2
                        sounds.lose_heart_sound.play()
                    if marioW.lives == 0:
                        i = 1
                        sounds.lose_game_sound.play()
                        lost = True 
                    goombaList.remove(goom)
    
#make a falling object every timeInterval seconds
clock.schedule_interval(makeObj, timeInterval)

pgzrun.go()
