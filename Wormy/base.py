#-*- coding = utf-8 -*-
#-*- coding = utf-8 -*-

import sys,random
import pygame
from pygame.locals import *
from constant import *

import copy
TOUP = 'up'
TOLEFT = 'left'
TORIGHT = 'right'
TODOWN = 'down'


class Grid(object):
    def __init__(self,surface,row, col):
        self.rowCount = row
        self.colCount = col
        print col
        self.surface = surface
        
        self.width = surface.get_width()
        self.height = surface.get_height()
        
        stepx = self.width / (1.0 * col)
        stepy = self.height / (1.0 *row)
        assert stepx == stepy
        self.cellSize = stepx
    def show(self):
        x = [self.cellSize * i for i in range(self.colCount + 1)]
        y = [self.cellSize * i for i in range(self.rowCount + 1)]
        line_width = 1
        for y_pos in y:
            pygame.draw.line(self.surface,GRAY , (0, y_pos), (self.width, y_pos), line_width)
        for x_pos in x:
            pygame.draw.line(self.surface,GRAY , (x_pos, 0), (x_pos, self.height), line_width)

class Wormy():
    def __init__(self):
        self.body = [[0,0], [0,0], [0,0]]
        self.tail = [0,0]
        self.grid = None
        self.moveTo = TOLEFT
    def addToGrid(self, grid):
        self.grid = grid
        HEAD = 0
        surface = grid.surface
        row = grid.rowCount
        col = grid.colCount
        assert( (row > 10) and (col > 10))
        headx = random.randint(5, col - 5)
        heady = random.randint(5, row - 5)
        self.body[HEAD] = [headx, heady]
        self.body[HEAD+1] = [headx+1, heady]
        self.body[HEAD+2] = [headx+ 2, heady]
        self.show()
        
    def show(self):
        if not self.grid:
            return
        
        for pos in self.body:
            row = pos[0]
            col = pos[1]
            topx = self.grid.cellSize * row
            topy = self.grid.cellSize * col
            width = self.grid.cellSize
            height = self.grid.cellSize
            rect = pygame.Rect(topx,topy, width, height)
            pygame.draw.rect(self.grid.surface, WHITE, rect, 0)
            pygame.draw.rect(self.grid.surface, YELLOW, rect, 2)
    def move(self, moveTo):
        TAIL = -1
        HEAD = 0
        self.tail = copy.deepcopy(self.body[TAIL])
        del self.body[TAIL]
        
        head = self.body[HEAD]
        if moveTo == TOLEFT:
            new_head = [head[0] - 1 ,head[1]]
            self.body.insert(0, new_head)
        elif moveTo == TORIGHT:
            new_head = [head[0] + 1 ,head[1]]
            self.body.insert(0, new_head)
        elif moveTo == TOUP:
            new_head = [head[0] ,head[1] - 1]
            self.body.insert(0, new_head )
        elif moveTo == TODOWN:
            new_head = [head[0],head[1] + 1]
            self.body.insert(0, new_head)
            
    def eat(self):
        TAIL = -1
        self.body.insert(TAIL, self.tail)
        
    def isDied(self):
        HEAD = 0
        head = self.body[HEAD]
        MAXROW = self.grid.rowCount
        MaxCOL = self.grid.colCount
        if (head[0] < 0) or (head[0]>=MaxCOL): 
            return True
        if(head[1] <0) or(head[1]>= MAXROW):
            return True
        for item in self.body[1:]:
            if (head[0] == item[0]) and (head [1] == item[1]):
                return True
        return False
    def reset(self):
        grid = self.grid
        HEAD = 0
        surface = grid.surface
        row = grid.rowCount
        col = grid.colCount
        assert( (row > 10) and (col > 10))
        headx = random.randint(5, col - 5)
        heady = random.randint(5, row - 5)
        self.body[HEAD] = [headx, heady]
        self.body[HEAD+1] = [headx+1, heady]
        self.body[HEAD+2] = [headx+ 2, heady]
        self.show()
        
class Food(object):
    def __init__(self):
        self.x = 0
        self.y = 0
        self.grid = None
    def addToGrid(self,grid):
        self.grid = grid
        MaxRow = grid.rowCount
        MaxCol = grid.colCount
        self.x = random.randint(1, MaxCol - 1)
        self.y = random.randint(1, MaxRow - 1)
        self.show()
    def changePosition(self):
        if self.grid:
            grid = self.grid
            MaxRow = grid.rowCount
            MaxCol = grid.colCount
            self.x = random.randint(1, MaxCol - 1)
            self.y = random.randint(1, MaxRow - 1)
            print self.x,self.y
    
    def show(self):
        if not self.grid:
            return
        cellSize = self.grid.cellSize
        topx = cellSize * self.x
        topy = cellSize * self.y
        width = cellSize
        height = cellSize
        rect = pygame.Rect(topx,topy, width, height)
        pygame.draw.rect(self.grid.surface, BLUE, rect, 0)
        pygame.draw.rect(self.grid.surface, YELLOW, rect, 2)
def isHited(food, wormy):
    head = wormy.body[0]
    if (food.x == head[0]) and (food.y == head[1]):
        wormy.eat()
        food.changePosition()
def reset(surface,isWined):
    surface.fill(BLACK)
    fontobj = pygame.font.Font('freesansbold.ttf', 32)
    tetextSurfaceobj = None
    if isWined:
        tetextSurfaceobj = fontobj.render('Game Over', True, GREEN, BLUE)
    else:
        tetextSurfaceobj = fontobj.render('You Win', True, GREEN, BLUE)
    textrect = tetextSurfaceobj.get_rect()
    textrect.center = surface.get_rect().center
    surface.blit(tetextSurfaceobj,textrect)

    
    
    
          
if __name__ == '__main__':
    pygame.init()
    WIDTH = 640
    HEIGHT = 480
    CELL_SIZE = 20
    FPS = 30
    surface = pygame.display.set_mode((WIDTH, HEIGHT))
    grid = Grid(surface, HEIGHT/CELL_SIZE, WIDTH/CELL_SIZE)
    wormy = Wormy()
    wormy.addToGrid(grid)
    fpsClock = pygame.time.Clock()
    food = Food()
    food.addToGrid(grid)
    
    while True:
        surface.fill(BLACK)
        grid.show()
        wormy.show()
        food.show()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:   
                if event.key == K_UP:
                    wormy.move(TOUP)
                    
                if event.key == K_DOWN:
                    wormy.move(TODOWN)
                    
                if event.key == K_RIGHT:
                    wormy.move(TORIGHT)
                    
                if event.key == K_LEFT:
                    wormy.move(TOLEFT)
            isHited(food, wormy)
            if wormy.isDied():
                reset(surface, True)
                pygame.display.update()
                pygame.time.wait(2000)
                wormy.reset()
                food.changePosition()
                
                    
                
        pygame.display.update()
        fpsClock.tick(FPS)
        
        