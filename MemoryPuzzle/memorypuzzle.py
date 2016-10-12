#Memry Puzzle
#

import random, sys
import pygame as pyg
from pygame.locals import *

FPS = 30 
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
REVELSPEED = 8
BOXSIZE = 40
GAPSIZE = 10
BOARDWIDTH = 10
BOARDHEIGHT = 7

assert(BOARDWIDTH*BOARDHEIGHT%2)%2 == 0
XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * (BOXSIZE + GAPSIZE))) / 2)
YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * (BOXSIZE + GAPSIZE))) / 2)

#COLOR
GRAY = (100, 100, 100)
NAVYBLUE = (60, 60, 100)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 128, 0)
PURPLE = (255, 0 , 255)
CYAN = (0, 255, 255)
BGCOLOR = NAVYBLUE
LIGHTBGCOLOR = GRAY
BOXCOLOR = WHITE
HIGHLIGHTCOLOR = BLUE

DONUT = 'donut'
SQUARE = 'square'
DIAMOND = 'diamond'
LINES = 'lines'
OVAL = 'oval'

AllCOLOR = (RED,
            GREEN,
            BLUE,
            YELLOW,
            ORANGE,
            PURPLE,
            CYAN
            )
ALLSHAPES = (DONUT,
             SQUARE,
             DIAMOND,
             LINES,
             OVAL
             )
assert len(AllCOLOR) * len(ALLSHAPES) * 2 >= BOARDWIDTH * BOARDHEIGHT
def main():
    global FPSCLOCK, DISPLAYSURF
    pyg.init()
    FPSCLOCK = pyg.time.Clock()
    DISPLAYSURF = pyg.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    
    mousex = 0
    mousey = 0
    pyg.display.set_caption('MemoryGame')
    
    mainBoard = getRandomizedBoard()
    revealedBoxes = generateRevealedBoxesData(False)
    
    firstSelection = None
    DISPLAYSURF.fill(BGCOLOR)
    startGameAnimation(mainBoard)
    
    while True:
        mouseClicked = False
        DISPLAYSURF.fill(BGCOLOR)
        drawBoard(mainBoard, revealedBoxes)
        
        for event in pyg.event.get():
            
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pyg.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex,mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True
    
            boxx,boxy = getBoxAtPixel(mousex,mousey)
            
            if boxx!=None and boxy!=None:
                if not revealedBoxes[boxx][boxy]:
                    drawHightlightBox(boxx, boxy)
                 
                if not revealedBoxes[boxx][boxy] and mouseClicked:
                    revealedBoxesAnimation(mainBoard, [(boxx,boxy)]) 
                    revealedBoxes[boxx][boxy] = True
                    if firstSelection == None:   
                        firstSelection = (boxx,boxy)
                    else:
                        icon1shape,icon1color = getShapeAndColor(mainBoard, firstSelection[0], firstSelection[1])
                        icon2shape,icon2color = getShapeAndColor(mainBoard, boxx, boxy)
                        
                        if icon1shape != icon2shape or icon1color != icon2color:
                            pyg.time.wait(1000)
                            coverBoxesAnimation(mainBoard,
                                                [(firstSelection[0],firstSelection[1]),
                                                 (boxx, boxy)])
                            revealedBoxes[boxx][boxy] = False
                            revealedBoxes[firstSelection[0]][firstSelection[1]] = False
                        elif hasWon(revealedBoxes):
                            gameWonAnimation(mainBoard)
                            pyg.time.wait(2000)
                            
                            #reset
                            mainBoard = getRandomizedBoard()
                            revealedBoxes = generateRevealedBoxesData(False)
                            #show the fully unrevealed board ro asecond
                            drawBoard(mainBoard, revealedBoxes)
                            pyg.display.update()
                            pyg.time.wait(1000)
                            #replay
                            startGameAnimation(mainBoard)
                        firstSelection = None
                            
            pyg.display.update()
            FPSCLOCK.tick(FPS)
                            
def generateRevealedBoxesData(val):
    revealedBoxes = []
    for i in range(BOARDWIDTH):
        revealedBoxes.append([val]*BOARDHEIGHT)
    return revealedBoxes


def getRandomizedBoard():
    icons = []
    for color in AllCOLOR:
        for shape in ALLSHAPES:
            icons.append((shape, color))
    random.shuffle(icons)
    numIcomUsed = int(BOARDWIDTH * BOARDHEIGHT / 2)
    icons = icons[:numIcomUsed]*2
    random.shuffle(icons)
    #????????????
    board = []
    for x in range(BOARDWIDTH):
        column = []
        for y in range(BOARDHEIGHT):
            column.append(icons[0])
            del icons[0]
        board.append(column)
    return board


def splitIntGroupsOf(groupSize, theList):
    result = []
    for i in range(0, len(theList), groupSize):
        result.append(theList[i:i + groupSize])
    return result

def leftTopCoordsOfBox(boxx,boxy):
    left = boxx * (BOXSIZE + GAPSIZE) + XMARGIN
    top = boxy * (BOXSIZE + GAPSIZE) +YMARGIN
    return(left, top)


def getBoxAtPixel(x, y):
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            boxRect = pyg.Rect(left,top, BOXSIZE,BOXSIZE)
            if boxRect.collidepoint(x, y):
                return (boxx,boxy)
    return (None, None)
    
    
def drawIcon(shape, color, boxx, boxy):
    quarter = int(BOXSIZE * 0.25)
    half = int(BOXSIZE* 0.5)
    left, top = leftTopCoordsOfBox(boxx, boxy)
    
    #draw shapes
    if shape == DONUT:
        pyg.draw.circle(DISPLAYSURF, color, (left + half,top + half),half-5)
        pyg.draw.circle(DISPLAYSURF,BGCOLOR, (left + half,top + half), quarter -5)
    elif shape == SQUARE:
        pyg.draw.rect(DISPLAYSURF, color,(left + quarter, top + quarter,BOXSIZE-half,BOXSIZE - half))
    elif shape == DIAMOND:
        pyg.draw.polygon(DISPLAYSURF, color,
                        ((left + quarter, top), (left + BOXSIZE - 1, top + half),
                        (left + half, top + BOXSIZE - 1),(left,top + half)))
    elif shape == LINES:
        for i in range(0, BOXSIZE, 4):
            pyg.draw.line(DISPLAYSURF, color, (left, top+i), (left + i,top))
            pyg.draw.line(DISPLAYSURF, color, (left + i, top + BOXSIZE-1),(left+BOXSIZE -1, top + i))
    elif shape == OVAL:
        pyg.draw.ellipse(DISPLAYSURF, color, (left, top+quarter, BOXSIZE, half))
def getShapeAndColor(board, boxx, boxy):
    return board[boxx][boxy][0],board[boxx][boxy][1]


def drawBoxCovers(board, boxes, coverage):
    for box in boxes:
        left, top = leftTopCoordsOfBox(box[0], box[1])
        pyg.draw.rect(DISPLAYSURF, BGCOLOR, (left, top, BOXSIZE, BOXSIZE))
        shape, color = getShapeAndColor(board, box[0],box[1])
        drawIcon(shape, color, box[0], box[1])
        if coverage > 0:
            pyg.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, coverage, BOXSIZE))
    pyg.display.update()
    FPSCLOCK.tick()
    
def revealedBoxesAnimation(board, boxesToReveal):
    for coverage in range(BOXSIZE, -1, -REVELSPEED):
        drawBoxCovers(board, boxesToReveal, coverage)


def coverBoxesAnimation(board, boxesToCover):
    for coverage in range(0, BOXSIZE + REVELSPEED, REVELSPEED):
        drawBoxCovers(board, boxesToCover, coverage)


def drawBoard(board, revealed):
    
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            if not revealed[boxx][boxy]:
                pyg.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, BOXSIZE,BOXSIZE))
            else:
                shape, color = getShapeAndColor(board, boxx, boxy)
                drawIcon(shape, color, boxx, boxy)
def drawHightlightBox(boxx, boxy):
    left, top = leftTopCoordsOfBox(boxx, boxy)
    pyg.draw.rect(DISPLAYSURF, HIGHLIGHTCOLOR, (left-5, top-5, BOXSIZE+10, BOXSIZE+10), 4)


def startGameAnimation(board):
    
    coveredBoxes = generateRevealedBoxesData(False)
    boxes = []
    
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            boxes.append((x,y))
    random.shuffle(boxes)
    boxGroups = splitIntGroupsOf(8, boxes)
    
    drawBoard(board, coveredBoxes)
    for boxGroup in boxGroups:
        revealedBoxesAnimation(board, boxGroup)
        coverBoxesAnimation(board, boxGroup)


def gameWonAnimation(board):
    coveredBoxes = generateRevealedBoxesData(True)
    color1 = LIGHTBGCOLOR
    color2 = BGCOLOR
    for i in range(13):
        color1, color2 = color2,color1
        DISPLAYSURF.fill(color1)
        drawBoard(board, coveredBoxes)
        pyg.display.update()
        pyg.time.wait(300)
        
        
def hasWon(revealedBoxes):
    for i in revealedBoxes:
        if False in i:
            return False
        return True
        
                       
    

if __name__ == '__main__':
   
    main()
    pass