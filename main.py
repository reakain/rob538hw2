#!/usr/bin/env python3
import pygame
import random
from pygame import *
from grid import Agent, Target

BOUNDS = (10,5)    # (width,height)
T1 = (10,4)     # Target starting position (x, y)
AGENT = (random.randint(1,BOUNDS[0]),random.randint(1,BOUNDS[1]))

GridMult = 20
XDIM = 720
YDIM = 500
windowSize = [XDIM, YDIM]
GridTopLeft = ((XDIM-(BOUNDS[0]*GridMult))/2,(GridMult*2))
TRAINING_RUNS = 50
pygame.init()
fpsClock = pygame.time.Clock()
screen = pygame.display.set_mode(windowSize)
white = 255, 255, 255
black = 0, 0, 0
red = 255, 0, 0
green = 0, 255, 0
blue = 0, 0, 255
cyan = 0,180,105

agents = {Agent(AGENT,BOUNDS), Agent(AGENT,BOUNDS)}
target = Target(T1,BOUNDS)

def draw_grid():
    for x in range(BOUNDS[0]):
        for y in range(BOUNDS[1]):
            draw_square((x,y),black,white)
    for agent in agents:
        draw_square(agent.id,black,blue)
    draw_square(target.id,black,red)

def draw_square(topleft,border,fill):
    rx = GridTopLeft[0]+(topleft[0]*GridMult)
    ry = GridTopLeft[1]+(topleft[1]*GridMult)
    rect = pygame.Rect(rx,ry,GridMult,GridMult)
    pygame.draw.rect(screen,fill,rect)
    pygame.draw.rect(screen,border,rect,1)

def reset():
    global count
    AGENT = (random.randint(1,BOUNDS[0]),random.randint(1,BOUNDS[1]))
    agents = {Agent(AGENT,BOUNDS), Agent(AGENT,BOUNDS)}
    target = Target(T1,BOUNDS)
    screen.fill(white)
    draw_grid()
    count = 0

def iterate_time():
    target.move()
    for agent in agents:
        agent.move(target.id)

def new_run():
    AGENT = (random.randint(1,BOUNDS[0]),random.randint(1,BOUNDS[1]))
    for agent in agents:
        agent.new_run(AGENT)
    target = Target(T1,BOUNDS)

def found_target():
    for agent in agents:
        if(not agent.found_T):
            return False
    return True


if __name__ == "__main__":
    currentState = 'init'
    reset()

    while True:
        if currentState == 'init':
            print('waiting to start...')
            pygame.display.set_caption('press anywhere to start')
            fpsClock.tick(10)
        elif currentState == 'complete':
            pygame.display.set_caption('Completed training')
            print('training complete!')
            # save display to image
        elif currentState == 'training':
            # go through iterations
            pygame.display.set_caption('Training system...')
            if count < TRAINING_RUNS:
                draw_grid()
                if(not found_target()):
                    iterate_time()
                else:
                    count += 1
                    new_run()
            else:
                currentState = 'complete'
                draw_grid()

        elif currentState == 'running':
            pygame.display.set_caption('Using training results...')
            # go through and look at results?

        #handle events
        for e in pygame.event.get():
            if e.type == QUIT or (e.type == KEYUP and e.key == K_ESCAPE):
                sys.exit("Exiting")
            if e.type == MOUSEBUTTONDOWN:
                print('mouse down')
                if currentState == 'init':
                    print('starting!')
                    currentState = 'training'
                elif currentState != 'training':
                    currentState = 'init'
                    reset()


        pygame.display.update()
        fpsClock.tick(10000)
