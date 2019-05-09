# Rory Wagner
# Begun 5/7/2019
# This code creates a random maze, and draws it.
# We are currently working on a solver for the maze.
# We will also be implementing a character that can move throughout the maze.

from graphics import *
import random
import sys

M = 10
N = 10
CELL_SIZE = 50
MARGIN = 10
screen_x = M*CELL_SIZE + 2*MARGIN
screen_y = N*CELL_SIZE + 2*MARGIN

class Cell:
    def __init__(self):
        self.l = self.t = self.r = self.b = True
        self.visited = False

    def Draw(self, win, i,j):
        x1 = MARGIN + i*CELL_SIZE
        y1 = MARGIN + j*CELL_SIZE
        x2 = x1 + CELL_SIZE
        y2 = y1 + CELL_SIZE
        if self.l:
            line = Line( Point(x1,y1), Point(x1,y2) )
            line.draw(win)
        if self.t:
            line = Line( Point(x1,y1), Point(x2,y1) )
            line.draw(win)
        if self.r:
            line = Line( Point(x2,y1), Point(x2,y2) )
            line.draw(win)
        if self.b:
            line = Line( Point(x1,y2), Point(x2,y2) )
            line.draw(win)

class Maze:
    def __init__(self):
        self.cells = []
        for i in range(M):
            cellColumn = []
            for j in range(N):
                cellColumn.append(Cell())
            self.cells.append(cellColumn)
        self.VisitR(0,0)
        self.cells[0][0].t = False
        self.cells[M-1][N-1].b = False
        
    def VisitR(self, i,j):
        self.cells[i][j].visited = True
        while True:
            nexti = []
            nextj = []
            # determine which cells we could move to next
            if i>0 and not self.cells[i-1][j].visited: # left
                nexti.append(i-1)
                nextj.append(j)
            if i<M-1 and not self.cells[i+1][j].visited: # right
                nexti.append(i+1)
                nextj.append(j)
            if j>0 and not self.cells[i][j-1].visited: # up
                nexti.append(i)
                nextj.append(j-1)
            if j<N-1 and not self.cells[i][j+1].visited: # down
                nexti.append(i)
                nextj.append(j+1)

            if len(nexti) == 0:
                return # nowhere to go from here

            # randomly choose 1 direction to go
            index = random.randrange(len(nexti))
            ni = nexti[index]
            nj = nextj[index]

            # knock out walls between this cell and the next cell
            if ni == i+1: # right move
                self.cells[i][j].r = self.cells[i+1][j].l = False
            if ni == i-1: # left move
                self.cells[i][j].l = self.cells[i-1][j].r = False
            if nj == j+1: # down move
                self.cells[i][j].b = self.cells[i][j+1].t = False
            if nj == j-1: # up move
                self.cells[i][j].t = self.cells[i][j-1].b = False

            # recursively visit the next cell
            self.VisitR(ni,nj)
        
    def Draw(self, win):
        for i in range(M):
            for j in range(N):
                self.cells[i][j].Draw(win,i,j)
        

    # Write this method.
    # It should return True if this is the end cell, OR if it leads to the end cell.
    # It should return False if this is a loser cell.
    ###
    # i should be the column number
    # j should be the row number
    def SolveR(self, i, j):
        global M
        global N

        self.cells[i][j].visited = True

        index = M * i + j

        self.mMoves.append(index)

        if index == M * N - 1:
            return True
        
        #The first if statements at the beginning of the nests aren't letting anything through...
        #Need to understand what they are testing for.
        if self.cells[i][j].l and self.cells[i-1][j].visited:
            if self.SolveR(i - 1, j):
                return True

        if self.cells[i][j].r and self.cells[i+1][j].visited:
            if self.SolveR(i + 1, j):
                return True
        
        if self.cells[i][j].b and self.cells[i][j+1].visited:
            if self.SolveR(i, j + 1):
                return True

        if self.cells[i][j].t and self.cells[i][j-1].visited:
            if self.SolveR(i, j - 1):
                return True

        self.mMoves.pop()
        return False

    ###

    def Solve(self):
        global M
        global N
        #initializes mMoves array:
        self.mMoves = []
        #initializes all cells to not visited:
        for i in range(M):
            for j in range(N):
                self.cells[i][j].visited = False

        self.SolveR(0,0)

    # Write this method.
    def DrawSolution(self, win):
        global M
        global N
        print( self.mMoves)
        for i in range(len(self.mMoves)-1):
            index1 = self.mMoves[i]
            index2 = self.mMoves[i+1]
            i1 = index1 % M
            j1 = index1 // M
            i2 = index2 % M
            j2 = index2 // M
            x1 = int(MARGIN + (i1 + 0.5) * CELL_SIZE)
            y1 = int(MARGIN + (j1 + 0.5) * CELL_SIZE)
            x2 = int(MARGIN + (i2 + 0.5) * CELL_SIZE)
            y2 = int(MARGIN + (j2 + 0.5) * CELL_SIZE)
            line = Line(Point(x1, y1), Point(x2, y2))
            line.draw(win)
        
        # Now draw it graphically!

class CharacterBlock:
    def __init__(self):
        self.mX = 0
        self.mY = 0
        return
    
    def moveRight(self):
        global M
        self.mX += 1
        if self.mX >= M:
            self.mX -= M
        return
    
    def moveLeft(self):
        global M
        self.mX -= 1
        if self.mX < 0:
            self.mX += M
        return
    
    def moveUp(self):
        global N
        self.mY += 1
        if self.mY >= N:
            self.mY -= N
        return
    
    def moveDown(self):
        global N
        self.mY -= 1
        if self.mY < 0:
            self.mY += N
        return

    def DrawCharacter(self):
        # Immediate numbers here are used for adjusting to still see the walls.
        x1 = MARGIN + self.mX * CELL_SIZE + 1
        y1 = MARGIN + self.mY * CELL_SIZE + 1
        x2 = x1 + CELL_SIZE - 2
        y2 = y1 + CELL_SIZE - 2
        point1 = Point(x1, y1)
        point2 = Point(x1, y1)
        Rectangle(point1, point2)
           


def main():
    sys.setrecursionlimit(10000)
    win = GraphWin("Maze Solver", screen_x, screen_y)

    theMaze = Maze()
    theMaze.Draw(win)
    theMaze.Solve()

    mouseClick = win.getMouse()                   # get mouse click
    theMaze.DrawSolution(win)
    
    mouseClick = win.getMouse()                   # get mouse click
    win.close()
    return 0

main()

    
