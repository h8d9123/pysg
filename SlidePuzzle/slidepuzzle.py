#coding = utf-8
import pygame, sys, random
from pygame.locals import *

WIDTH = 640
HEIGHT = 480
CARDWIDTH = 50
CARDHEIGHT = 50
FPS = 30

ROW = 5
COL = 5
#COLOR
BLACK = (0, 0, 0)
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

class board(object):
    def __init__(self,row,col):
        self.colCount = row
        self.rowCount = col
        self.blankRow = 0
        self.blankCol = 0
        self.cards = []
        self.displaySurface = None
        self.cardWidth = 0
        self.cardHeight = 0
        self.createBoard(row, col)
        
    def createBoard(self,row,col):
        # row and col is unsignal int
        #assert row>0 and col>0, 'row and col is unsigned interger'
        
        self.cards = range(row * col)
        random.shuffle(self.cards)
        iblank = self.cards.index(0)
        self.blankRow = iblank / self.colCount
        self.blankCol = iblank % self.colCount
        
        
    def setDisplaySurface(self, displaySurface):
        self.displaySurface = displaySurface
        
        
    def moveUp(self):
        cards = self.cards
        if self.blankRow > 0:
            iBlank = self.blankRow * self.colCount + self.blankCol
            iCardTo = (self.blankRow -1) * self.colCount + self.blankCol
            cards[iCardTo], cards[iBlank] = cards[iBlank], cards[iCardTo]
            self.blankRow -= 1
    
    
    def moveDown(self):
        
        cards = self.cards
        if self.blankRow <self.rowCount:
            iBlank = self.blankRow * self.colCount + self.blankCol
            iCardTo = (self.blankRow + 1) * self.colCount + self.blankCol
            cards[iCardTo], cards[iBlank] = cards[iBlank], cards[iCardTo]
            self.blankRow += 1
     
            
    def moveRight(self):
        
        cards = self.cards
        if self.blankCol <self.colCount:
            iBlank = self.blankRow * self.colCount + self.blankCol
            iCardTo = self.blankRow * self.colCount + self.blankCol + 1
            cards[iCardTo], cards[iBlank] = cards[iBlank], cards[iCardTo]
            self.blankCol += 1
        
    
    def moveLeft(self):
     
        cards = self.cards
        if self.blankCol > 0:
            iBlank = self.blankRow * self.colCount + self.blankCol
            iCardTo = self.blankRow * self.colCount +self.blankCol - 1
            cards[iCardTo], cards[iBlank] = cards[iBlank], cards[iCardTo]
            self.blankCol -= 1
        
    
    def hasWon(self):
        
        for i in range(15):
            if self.cards[i] != (i + 1):
                return False
        return True
    
    def draw(self):
        assert self.displaySurface != None,'board need to be given display surface'
        
        pass  
    def pixelToIndex(self, pos):
        
        if pos[0] > self.cardWidth * self.colCount or pos[0] < 0:
            return (-1, -1)
        if pos[1] > self.cardHeight * self.rowCount or pos[1] < 0:
            return (-1, -1)
        
        col = pos[0]/self.cardWidth
        row = pos[1]/self.cardHeight
        print (row, col)
        return(row, col)
    
    def moveBlank(self,pos):
        row, col = self.pixelToIndex(pos)
        if row <0 or col < 0:
            return
        if row == self.blankRow:
            if col == self.blankCol - 1:
                self.moveLeft()
            if col == self.blankCol + 1:
                self.moveRight()
        if col == self.blankCol:
            if row == self.blankRow - 1:
                self.moveUp()
            if row == self.blankRow + 1:
                self.moveDown()
                
        
        
class Canvas(object):
    def __init__(self, displaySurface):
        
        self.displaySurface = displaySurface
        self.xMargin = 0
        self.yMargin = 0
        self.fps = 30
        self.fpsClock = None

    def drawLine(self, color, startPoint, endPoint, width = 1):
        pygame.draw.line(self.displaySurface,
                         color, startPoint, endPoint, width)
    def drawLines(self, color, closed, pointList, width=1):
        pygame.draw.lines(self.displaySurface,
                          color, closed, pointList, width)
    def drawRect(self,color,rectangleTuple, width = 0):
        pygame.draw.rect(self.displaySurface,
                         color, rectangleTuple, width)
    def drawCard(self,rect,number):
        fontObj = pygame.font.Font('freesansbold.ttf', 32)
        #font forecolor is black, bgcolog is white
        textSurf = fontObj.render('%s'%number, True, BLACK, WHITE)
        textRect = textSurf.get_rect()
        textRect.center = rect.center

        pygame.draw.rect(self.displaySurface,WHITE, (rect,),1)
        self.displaySurface.blit(textSurf,textRect)
        
    def drawBoard(self, board):
        row = board.rowCount
        col = board.colCount
        self.displaySurface.fill(WHITE)
        for index in range(row*col):
            
            leftTopX = self.xMargin + board.cardWidth*(index %row)
            leftTopY = self.yMargin + board.cardHeight*(index/row)

            rightDownX = board.cardWidth
            rightDownY = board.cardHeight
            rect = pygame.Rect(leftTopX,leftTopY, rightDownX, rightDownY)
            border = pygame.Rect(leftTopX,leftTopY, rightDownX, rightDownY)
            
            self.drawCard(rect, board.cards[index])
            pygame.draw.rect(self.displaySurface, BLUE, border, 1)
    def pixelToLocal(self,pos):
        
        localPos = (pos[0] - self.xMargin, pos[1] - self.yMargin)
        if pos[0] < 0:
            return (-1, -1)
        if pos[1] < 0:
            return (-1, -1)
    
        return localPos
            
    
if __name__ == '__main__':
    pygame.init()
    displaySurface = pygame.display.set_mode((WIDTH, HEIGHT))
    displaySurface.fill(WHITE)
    canvas = Canvas(displaySurface)
    canvas.fps = FPS
    canvas.fpsClock = pygame.time.Clock()
    board = board(ROW, COL)
    board.cardHeight = CARDHEIGHT
    board.cardWidth = CARDWIDTH
    assert(WIDTH - board.colCount * board.cardWidth > 0)
    assert(HEIGHT - board.rowCount * board.cardHeight > 0)
    canvas.xMargin = (WIDTH -board.colCount * board.cardWidth)/2
    canvas.yMargin = (HEIGHT - board.rowCount * board.cardHeight)/2
    
    canvas.drawBoard(board)
    while True:
        
        for event in pygame.event.get():
            pygame.display.update()
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONUP:
                mouseX, mouseY = event.pos
                pos = canvas.pixelToLocal(event.pos)
                board.moveBlank(pos)
                canvas.drawBoard(board)
                
        pygame.display.update()
        canvas.fpsClock.tick(canvas.fps)
        
        
        