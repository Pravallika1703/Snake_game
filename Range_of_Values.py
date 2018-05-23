# Wormy (a Nibbles clone)
# By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license

import random, pygame, sys
from pygame.locals import *
import threading

FPS = 5
WINDOWWIDTH = 600
WINDOWHEIGHT = 600
CELLSIZE = 20
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size."
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size."
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)

#             R    G    B
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
GREEN     = (  0, 255,   0)
DARKGREEN = (  0, 155,   0)
DARKGRAY  = ( 40,  40,  40)
LIGHTPINK      = ( 255,204,255)
PINK=(204,0,153)
LGHTBLUE=(153,204,255)
BLUE=(0,51,204)
YELLOW    = (255, 128,0)
CYAN      =(153,255,255)
color1= (199,172,146)
color2= (205,83,59)
color3=(160,154,188)
color4=(182,166,202)

BGCOLOR = BLACK

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'
HEAD = 0 # syntactic sugar: index of the worm's head

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('Snake Game')

    showStartScreen()
    while True:
        runGame()
        showGameOverScreen()



def runGame():
    # Set a random start point.
    startx = random.randint(5, CELLWIDTH - 6)
    starty = random.randint(5, CELLHEIGHT - 6)
    startx1 = random.randint(5, CELLWIDTH - 6)
    starty1 = random.randint(5, CELLHEIGHT - 6)
    score1=score2 = n1=n2=0;

    wormCoords = [{'x': startx,     'y': starty},
                  {'x': startx - 1, 'y': starty},
                  {'x': startx - 2, 'y': starty}]

    wormCoords1 = [{'x': startx1, 'y': starty1},
                  {'x': startx1 - 1, 'y': starty1},
                  {'x': startx1 - 2, 'y': starty1}]

    direction = RIGHT
    direction1=RIGHT
    # Start the apple in a random place.
    apple = getRandomLocation()
    apple1 = getRandomLocation()
    apple2 = getRandomLocation()
    apple3 = getRandomLocation()
    first=second=third=four=0
    while True: # main game loop
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if (event.key == K_LEFT or event.key == K_KP4) and direction != RIGHT:
                    direction = LEFT
                elif (event.key == K_RIGHT or event.key == K_KP6) and direction != LEFT:
                    direction = RIGHT
                elif (event.key == K_UP or event.key == K_KP8) and direction != DOWN:
                    direction = UP
                elif (event.key == K_DOWN or event.key == K_KP2) and direction != UP:
                    direction = DOWN
                if (event.key == K_j or event.key == K_KP4) and direction1 != RIGHT:
                    direction1 = LEFT
                elif (event.key == K_l or event.key == K_KP6) and direction1 != LEFT:
                    direction1 = RIGHT
                elif (event.key == K_i or event.key == K_KP8) and direction1 != DOWN:
                    direction1 = UP
                elif (event.key == K_k or event.key == K_KP2) and direction1 != UP:
                    direction1 = DOWN
                elif event.key == K_ESCAPE:
                    terminate()

        # check if the worm has hit itself or the edge

        if wormCoords[HEAD]['x'] == CELLWIDTH or wormCoords[HEAD]['y'] == CELLHEIGHT:
            drawScore(len(wormCoords) - 3 + score1-2)
            pygame.display.update()
            return # game over
        if wormCoords[HEAD]['x'] == -1 or wormCoords[HEAD]['y'] == -1:
            return

        for wormBody in wormCoords[1:]:
            if wormBody['x'] == wormCoords[HEAD]['x'] and wormBody['y'] == wormCoords[HEAD]['y']:
                return # game over
            if wormBody['x'] == wormCoords1[HEAD]['x'] and wormBody['y'] == wormCoords1[HEAD]['y']:
                drawScore1(len(wormCoords1) - 3 + score2-2)
                pygame.display.update()
                return # game over

        # check if te worm hits other snakes
       # if wormCoords[HEAD]['x'] == wormCoords1[HEAD]['x'] or wormCoords[HEAD]['x'] == wormCoords1[HEAD]['y'] or wormCoords[HEAD]['y'] == wormCoords1[HEAD]['x'] or wormCoords[HEAD]['y'] == wormCoords1[HEAD]['y']:
            #return  # game over
        #for wormBody in wormCoords[1:]:
            #for wormBody1 in wormCoords1[1:]:
               # if wormBody['x'] == wormBody1['x'] and wormBody['y'] == wormBody1['y']:
                    #return  # game over


        if wormCoords1[HEAD]['x'] == CELLWIDTH or wormCoords1[HEAD]['y'] == CELLHEIGHT:
            drawScore1(len(wormCoords1) - 3 + score2-2)
            pygame.display.update()
            return # game over
        if wormCoords1[HEAD]['x'] == -1 or wormCoords1[HEAD]['y'] == -1:
            return
        for wormBody in wormCoords1[1:]:
            if wormBody['x'] == wormCoords1[HEAD]['x'] and wormBody['y'] == wormCoords1[HEAD]['y']:
                return # game over
            if wormBody['x'] == wormCoords[HEAD]['x'] and wormBody['y'] == wormCoords[HEAD]['y']:
                drawScore(len(wormCoords) - 3 + score1-2)
                pygame.display.update()
                return # game over




        # check if worm has eaten an apply

        if wormCoords[HEAD]['x'] == apple['x'] and wormCoords[HEAD]['y'] == apple['y']:
            # don't remove worm's tail segment
            apple = getRandomLocation() # set a new apple somewhere
            first=0
        elif wormCoords[HEAD]['x'] == apple1['x'] and wormCoords[HEAD]['y'] == apple1['y']:
            apple1 = getRandomLocation()
            second=0
        elif wormCoords[HEAD]['x'] == apple2['x'] and wormCoords[HEAD]['y'] == apple2['y']:
            apple2 = getRandomLocation()
            third=0
        elif wormCoords[HEAD]['x'] == apple3['x'] and wormCoords[HEAD]['y'] == apple3['y']:
            apple3 = getRandomLocation()
            fourth=0
        else:
            del wormCoords[-1] # remove worm's tail segment


        if wormCoords1[HEAD]['x'] == apple['x'] and wormCoords1[HEAD]['y'] == apple['y']:
            # don't remove worm's tail segment
            apple = getRandomLocation() # set a new apple somewhere
            first=0
        elif wormCoords1[HEAD]['x'] == apple1['x'] and wormCoords1[HEAD]['y'] == apple1['y']:
            apple1 = getRandomLocation()
            second=0
        elif wormCoords1[HEAD]['x'] == apple2['x'] and wormCoords1[HEAD]['y'] == apple2['y']:
            apple2 = getRandomLocation()
            third=0
        elif wormCoords1[HEAD]['x'] == apple3['x'] and wormCoords1[HEAD]['y'] == apple3['y']:
            apple3 = getRandomLocation()
            four=0
        else:
            del wormCoords1[-1] # remove worm's tail segment

        # move the worm by adding a segment in the direction it is moving
        if direction == UP:
            newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] - 1}
        elif direction == DOWN:
            newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] + 1}
        elif direction == LEFT:
            newHead = {'x': wormCoords[HEAD]['x'] - 1, 'y': wormCoords[HEAD]['y']}
        elif direction == RIGHT:
            newHead = {'x': wormCoords[HEAD]['x'] + 1, 'y': wormCoords[HEAD]['y']}
        wormCoords.insert(0, newHead)
        if direction1 == UP:
            newHead1 = {'x': wormCoords1[HEAD]['x'], 'y': wormCoords1[HEAD]['y'] - 1}
        elif direction1 == DOWN:
            newHead1 = {'x': wormCoords1[HEAD]['x'], 'y': wormCoords1[HEAD]['y'] + 1}
        elif direction1 == LEFT:
            newHead1 = {'x': wormCoords1[HEAD]['x'] - 1, 'y': wormCoords1[HEAD]['y']}
        elif direction1 == RIGHT:
            newHead1= {'x': wormCoords1[HEAD]['x'] + 1, 'y': wormCoords1[HEAD]['y']}
        wormCoords1.insert(0, newHead1)

        DISPLAYSURF.fill(BGCOLOR)
        drawGrid()
        drawWorm(wormCoords)
        drawWorm1(wormCoords1)

        drawApple(apple,GREEN)
        drawApple(apple1,GREEN)
        drawApple(apple2,GREEN)
        drawApple(apple3,GREEN)

        if(first>50):
            apple = getRandomLocation()
            drawApple(apple, GREEN)
            first=0
        if(second>100):
            apple1 = getRandomLocation()
            drawApple(apple1, GREEN)
            second=0
        if(third>150):
            apple2 = getRandomLocation()
            drawApple(apple2, GREEN)
            third=0
        if(four>200):
            apple3 = getRandomLocation()
            drawApple(apple3, GREEN)
            four=0

        drawScore(len(wormCoords) - 3+score1)
        drawScore1(len(wormCoords1) - 3+score2)
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        first = first+1;
        second = second + 1;
        third = third + 1;
        four = four + 1;

def drawPressKeyMsg():
    pressKeySurf = BASICFONT.render('Press a key to play.', True, DARKGRAY)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 30)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)


def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()

    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key


def showStartScreen():
    titleFont = pygame.font.Font('freesansbold.ttf', 100)
    titleSurf1 = titleFont.render('Welcome!', True, CYAN , PINK)
    titleSurf2 = titleFont.render('Snake Game!', True, YELLOW)

    degrees1 = 0
    degrees2 = 0
    while True:
        DISPLAYSURF.fill(BGCOLOR)
        rotatedSurf1 = pygame.transform.rotate(titleSurf1, degrees1)
        rotatedRect1 = rotatedSurf1.get_rect()
        rotatedRect1.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf1, rotatedRect1)

        rotatedSurf2 = pygame.transform.rotate(titleSurf2, degrees2)
        rotatedRect2 = rotatedSurf2.get_rect()
        rotatedRect2.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf2, rotatedRect2)

        drawPressKeyMsg()

        if checkForKeyPress():
            pygame.event.get() # clear event queue
            return
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        degrees1 += 3 # rotate by 3 degrees each frame
        degrees2 += 7 # rotate by 7 degrees each frame


def terminate():
    pygame.quit()
    sys.exit()


def getRandomLocation():
    return {'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)}


def showGameOverScreen():
    gameOverFont = pygame.font.Font('freesansbold.ttf', 150)
    gameSurf = gameOverFont.render('Game', True, WHITE)
    overSurf = gameOverFont.render('Over', True, WHITE)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (WINDOWWIDTH / 2, 10)
    overRect.midtop = (WINDOWWIDTH / 2, gameRect.height + 10 + 25)

    DISPLAYSURF.blit(gameSurf, gameRect)
    DISPLAYSURF.blit(overSurf, overRect)
    drawPressKeyMsg()
    pygame.display.update()
    pygame.time.wait(5000)
    checkForKeyPress() # clear out any key presses in the event queue

    while True:
        if checkForKeyPress():
            pygame.event.get() # clear event queue
            return

def drawScore(score):

    scoreSurf = BASICFONT.render('Score1: %s' % (score), True, WHITE)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 120, 10)
    scoreSurf1 = BASICFONT.render('Score1:dddddddddddddddddddddd', True, WHITE)
    scoreRect1 = scoreSurf1.get_rect()
    scoreRect1.topleft = (WINDOWWIDTH - 120, 10)
    DISPLAYSURF.fill(DARKGRAY,scoreRect1)
    DISPLAYSURF.blit(scoreSurf, scoreRect)

def drawScore1(score):
    scoreSurf = BASICFONT.render('Score2: %s' % (score), True, WHITE)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 120, 40)
    scoreSurf1 = BASICFONT.render('Score:dddddddddddddddddddddd', True, WHITE)
    scoreRect1 = scoreSurf1.get_rect()
    scoreRect1.topleft = (WINDOWWIDTH - 120, 40)
    DISPLAYSURF.fill(DARKGRAY, scoreRect1)
    DISPLAYSURF.blit(scoreSurf, scoreRect)



def drawWorm(wormCoords):
    for coord in wormCoords:
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        wormSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, LIGHTPINK, wormSegmentRect)
        wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
        pygame.draw.rect(DISPLAYSURF, PINK, wormInnerSegmentRect)

def drawWorm1(wormCoords):
    for coord in wormCoords:
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        wormSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, LGHTBLUE, wormSegmentRect)
        wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
        pygame.draw.rect(DISPLAYSURF, BLUE, wormInnerSegmentRect)

def drawApple(coord,colorapple):
    x = coord['x'] * CELLSIZE
    y = coord['y'] * CELLSIZE
    appleRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    pygame.draw.rect(DISPLAYSURF, colorapple, appleRect)


def drawGrid():
    for x in range(0, WINDOWWIDTH, CELLSIZE): # draw vertical lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE): # draw horizontal lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WINDOWWIDTH, y))


if __name__ == '__main__':
    main()