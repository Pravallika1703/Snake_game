# Wormy (a Nibbles clone)
# By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license

import random, pygame, sys
from pygame.locals import *
import math
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
LIGHTPINK      = (255,204,255)
PINK=(204,0,153)
LGHTBLUE=(153,204,255)
BLUE=(0,51,204)
YELLOW    = (255, 128,0)
CYAN      =(153,255,255)
color1= (199,172,146)
color2= (205,83,59)
color3=(160,154,188)
color4=(182,166,202)

Colors=[[(255,204,255),(204,0,153)],[(153,204,255),(0,51,204)],[(255,255,204),(255,255,51)],[(204,255,255),(51,255,255)],[(255,229,204),(255,153,51)],[(255,204,204),(255,51,51)]]
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
    aworm=[]
    score=[0,0]
    aworm.append( [{'x': startx,     'y': starty},
                  {'x': startx - 1, 'y': starty},
                  {'x': startx - 2, 'y': starty}])

    aworm.append([{'x': startx1, 'y': starty1},
                  {'x': startx1 - 1, 'y': starty1},
                  {'x': startx1 - 2, 'y': starty1}])

    direction = RIGHT
    direction=[]
    direction.append(RIGHT)
    direction.append(RIGHT)
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
               if event.key == K_ESCAPE:
                    terminate()
        j=0


        for worms in aworm:
          distance1= math.sqrt(pow(worms[HEAD]['x']-apple['x'],2)+pow(worms[HEAD]['y']-apple['y'],2))
          distance2= math.sqrt(pow(worms[HEAD]['x']-apple1['x'],2)+pow(worms[HEAD]['y']-apple1['y'],2))
          distance3= math.sqrt(pow(worms[HEAD]['x'] - apple2['x'], 2) + pow(worms[HEAD]['y'] - apple2['y'], 2))
          distance4=math.sqrt(pow(worms[HEAD]['x']-apple3['x'],2)+pow(worms[HEAD]['y']-apple3['y'],2))
          if( distance1<=distance2 and distance1 <=distance3 and distance1<=distance4):
              if(worms[HEAD]['x']<apple['x']):
                  if(worms[HEAD]['y']==apple['y'] and direction[j]!=LEFT):
                      direction[j]=RIGHT
                  elif(worms[HEAD]['y']<apple['y'] and direction[j]!=UP):
                      direction[j]=DOWN
                  elif(direction[j]!=DOWN):
                      direction[j]=UP
              else:
                  if (worms[HEAD]['y'] == apple['y'] and direction[j] != RIGHT):
                      direction[j] = LEFT
                  elif (worms[HEAD]['y'] < apple['y'] and direction[j] != UP):
                      direction[j] = DOWN
                  elif (direction[j] != DOWN):
                      direction[j] = UP
          elif (distance2 <= distance1 and distance2 <= distance3 and distance2 <= distance4):
              if (worms[HEAD]['x'] < apple1['x']):
                  if (worms[HEAD]['y'] == apple1['y'] and direction[j] != LEFT):
                      direction[j] = RIGHT
                  elif (worms[HEAD]['y'] < apple1['y'] and direction[j] != UP):
                      direction[j] = DOWN
                  elif (direction[j] != DOWN):
                      direction[j] = UP
              else:
                  if (worms[HEAD]['y'] == apple1['y'] and direction[j] != RIGHT):
                      direction[j] = LEFT
                  elif (worms[HEAD]['y'] < apple1['y'] and direction[j] != UP):
                      direction[j] = DOWN
                  elif (direction[j] != DOWN):
                      direction[j] = UP
          if (distance3<= distance2 and distance3 <= distance1 and distance3 <= distance4):
              if (worms[HEAD]['x'] < apple2['x']):
                  if (worms[HEAD]['y'] == apple2['y'] and direction[j] != LEFT):
                      direction[j] = RIGHT
                  elif (worms[HEAD]['y'] < apple2['y'] and direction[j] != UP):
                      direction[j] = DOWN
                  elif (direction[j] != DOWN):
                      direction[j] = UP
              else:
                  if (worms[HEAD]['y'] == apple2['y'] and direction[j] != RIGHT):
                      direction[j] = LEFT
                  elif (worms[HEAD]['y'] < apple2['y'] and direction[j] != UP):
                      direction[j] = DOWN
                  elif (direction[j] != DOWN):
                      direction[j] = UP
          else:
              if (worms[HEAD]['x'] < apple3['x']):
                  if (worms[HEAD]['y'] == apple3['y'] and direction[j] != LEFT):
                      direction[j] = RIGHT
                  elif (worms[HEAD]['y'] < apple3['y'] and direction[j] != UP):
                      direction[j] = DOWN
                  elif (direction[j] != DOWN):
                      direction[j] = UP
              else:
                  if (worms[HEAD]['y'] == apple3['y'] and direction[j] != RIGHT):
                      direction[j] = LEFT
                  elif (worms[HEAD]['y'] < apple3['y'] and direction[j] != UP):
                      direction[j] = DOWN
                  elif (direction[j] != DOWN):
                      direction[j] = UP

          if worms[HEAD]['x']>=CELLWIDTH-2:
            if worms[HEAD]['y']<CELLHEIGHT//2 and direction[j]!=UP:
                direction[j]=DOWN
            elif direction[j]!=DOWN:
                direction[j]=UP
          if worms[HEAD]['y']>=CELLHEIGHT-2:
             if worms[HEAD]['x']>CELLWIDTH//2 and direction[j]!=RIGHT:
                direction[j]=LEFT
             elif direction[j]!=LEFT:
                direction[j]=RIGHT
          if worms[HEAD]['x']<=2:
              if worms[HEAD]['y'] < CELLHEIGHT // 2 and direction[j] != UP:
                  direction[j] = DOWN
              elif direction[j] != DOWN:
                  direction[j] = UP
          if worms[HEAD]['y'] <= 2:
              if worms[HEAD]['x'] > CELLWIDTH // 2 and direction[j] != RIGHT:
                  direction[j] = LEFT
              elif direction[j] != LEFT:
                  direction[j] = RIGHT
          j=j+1


        i=0
        # check if the worm has hit itself or the edge
        for wormCoords in aworm:
            if wormCoords[HEAD]['x'] == CELLWIDTH or wormCoords[HEAD]['y'] == CELLHEIGHT:
                #drawScore(len(wormCoords) - 3 + score1-2)
                pygame.display.update()
                return # game over
            if wormCoords[HEAD]['x'] == -1 or wormCoords[HEAD]['y'] == -1:
               return
        k=0
        for index1,wormCoords in enumerate(aworm):
            for wormBody in wormCoords[1:]:
                if wormBody['x'] == wormCoords[HEAD]['x'] and wormBody['y'] == wormCoords[HEAD]['y']:
                    return  # game over

            for index2,wormCoords1 in enumerate(aworm):
                if (index1!= index2):
                    if wormCoords[HEAD]['x'] == wormCoords1[HEAD]['x'] and wormCoords[HEAD]['y'] == wormCoords1[HEAD]['y']:
                       return
                    for wormBody in wormCoords[1:]:
                       if wormBody['x'] == wormCoords1[HEAD]['x'] and wormBody['y'] == wormCoords1[HEAD]['y']:
                           #drawScore1(len(wormCoords1) - 3 + score2-2)
                           pygame.display.update()
                           return # game over


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
                  four=0
            else:
                  del wormCoords[-1] # remove worm's tail segmen
            print("directin of %d: %s" %(k,direction[k]))
            if direction[k] == UP:
                 newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] - 1}
            elif direction[k] == DOWN:
                 newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] + 1}
            elif direction[k] == LEFT:
                  newHead = {'x': wormCoords[HEAD]['x'] - 1, 'y': wormCoords[HEAD]['y']}
            elif direction[k] == RIGHT:
                  newHead = {'x': wormCoords[HEAD]['x'] + 1, 'y': wormCoords[HEAD]['y']}
            wormCoords.insert(0, newHead)
            if(len(wormCoords)>=10):
                j=len(wormCoords)//2
                a = []
                while j<len(wormCoords):
                    del wormCoords[j]
                aworm.append([{'x': startx,'y': starty},
                  {'x': startx - 1, 'y': starty},
                  {'x': startx - 2, 'y': starty}])
                score.append(0)
            score[i]=len(wormCoords) - 3+score1
            i=i+1
            k=k+1

        DISPLAYSURF.fill(BGCOLOR)
        drawGrid()
        drawWorm(aworm,Colors)
        drawApple(apple,GREEN)
        drawApple(apple1,GREEN)
        drawApple(apple2,GREEN)
        drawApple(apple3,GREEN)

        if(first>50):
            apple = getRandomLocation()
            drawApple(apple, GREEN)
            first=0
        if (second > 100):
             apple1 = getRandomLocation()
             drawApple(apple1, GREEN)
             second = 0
        if (third > 150):
             apple2 = getRandomLocation()
             drawApple(apple2, GREEN)
             third = 0
        if (four > 200):
             apple3 = getRandomLocation()
             drawApple(apple3, GREEN)
             four = 0
        drawScore(score)
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        first = first+1;
        second = second + 1;
        third = third + 1;
        four = four + 1

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
    c1=CELLWIDTH/2
    c2=CELLHEIGHT/2
    return {'x': random.randint(0, c1- 1), 'y': random.randint(0, c2 - 1)}


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

def drawScore(scores):
    i=0
    while i<len(scores):
        scoreSurf = BASICFONT.render('Score %d: %s' % (i+1,scores[i]), True, WHITE)
        scoreRect = scoreSurf.get_rect()
        scoreRect.topleft = (WINDOWWIDTH - 120, (i+1)*20)
        scoreSurf1 = BASICFONT.render('Score %d:dddddddddddddddddddddd' %(i+1), True, WHITE)
        scoreRect1 = scoreSurf1.get_rect()
        scoreRect1.topleft = (WINDOWWIDTH - 120, (i+1)*20)
        DISPLAYSURF.fill(DARKGRAY,scoreRect1)
        DISPLAYSURF.blit(scoreSurf, scoreRect)
        i=i+1

def drawScore1(score):
    scoreSurf = BASICFONT.render('Score2: %s' % (score), True, WHITE)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 120, 40)
    scoreSurf1 = BASICFONT.render('Score:dddddddddddddddddddddd', True, WHITE)
    scoreRect1 = scoreSurf1.get_rect()
    scoreRect1.topleft = (WINDOWWIDTH - 120, 40)
    DISPLAYSURF.fill(DARKGRAY, scoreRect1)
    DISPLAYSURF.blit(scoreSurf, scoreRect)



def drawWorm(aworm,Colors):
    for wormCoords,color in zip(aworm,Colors):
        for coord in wormCoords:
            x = coord['x'] * CELLSIZE
            y = coord['y'] * CELLSIZE
            wormSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
            pygame.draw.rect(DISPLAYSURF, color[0], wormSegmentRect)
            wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
            pygame.draw.rect(DISPLAYSURF, color[1], wormInnerSegmentRect)


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