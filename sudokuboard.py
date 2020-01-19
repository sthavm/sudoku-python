import random
import layouts
import copy

class SudokuBoard():
    def __init__(self, index='random', puzzle=None):
        if index == 'random':
            self.layout = copy.deepcopy(layouts.layouts[random.randint(0,len(layouts.layouts)-1)])
        elif index == 'generate':
            pass
        else:
            self.layout = copy.deepcopy(layouts.layouts[index])
        self.listEmptyCells()
        self.setDomains()
    
    #def generatePuzzle(self):


    #Print out visual representation of board
    def print(self):
        for i in range(0,9):
            for j in range(0,9):
                visibleString = self.layout[i][j]
                if visibleString == 'x': visibleString = ' '
                if j==0:
                    print('\n'+str(visibleString)+' ', end='')
                elif j%3 == 2 and j != 8:
                    print(str(visibleString)+' | ', end='')
                else:
                    print(str(visibleString)+' ', end='')
            if i%3 == 2 and i != 8:
                print("\n------+-------+------", end='')
        print('\n')

    #Find an empty cell if there is one
    def findEmptyCell(self):
        for i in range(0,9):
            for j in range(0,9):
                if self.layout[i][j] == 'x':
                    return (i,j)
        return False
    
    def listEmptyCells(self):
        self.emptyCells = []
        for i in range(0,9):
            for j in range(0,9):
                if self.layout[i][j] == 'x':
                    self.emptyCells.append((i,j))
                    
    def setDomains(self):
        self.domains = dict()
        for row,col in self.emptyCells:
            for num in range(1,10):
                if self.isValid(num,row,col):
                    if (row,col) in self.domains:
                        self.domains[(row,col)].append(num)
                    else:
                        self.domains[(row,col)] = [num]

    
    #Check if a given assignment is valid
    def isValid(self,num,row,col):
        #Check if the cell is empty
        if self.layout[row][col] != 'x':
            return False
        #Check if input makes sense (if this ever becomes interactive)
        if num < 1 or num > 9:
            return False
        #Check if the number is already in that row
        if num in self.layout[row]:
            return False
        #Check if the number is already in that column
        for k in range(0,9):
            if num == self.layout[k][col]:
                return False
        #Check if the number is already in that 3x3 block
        for k in range(row-row%3,row-row%3+3):
            for l in range(col-col%3,col-col%3+3):
                if num == self.layout[k][l]:
                    return False
        return True
    
    #Solve the puzzle
    def solve(self,method='backtracking'):
        if method=='backtracking':
            if not self.findEmptyCell():
                return True
            row,col = self.findEmptyCell()
            for i in range(1,10):
                if self.isValid(i,row,col):
                    self.layout[row][col] = i
                    if self.solve():
                        return True
                    self.layout[row][col] = 'x'
            return False
        elif method=='forwardchecking':
            if not self.findEmptyCell():
                return True
            row,col = self.chooseLRV()
            for i in self.domains[(row,col)]:
                if self.isValid(i,row,col):
                    self.layout[row][col] = i
                    self.domains[(row,col)].remove((i))
                    if self.solve():
                        return True
                    self.layout[row][col] = 'x'
                    self.domains[(row,col)].append((i))
            return False

    def chooseLRV(self):
        min = float('inf')
        minCell = None
        for key in self.domains:
            if (n := len(self.domains[key])) < min:
                min = n
                minCell = key
        return minCell




board = SudokuBoard(1)
board.print()
board.solve('backtracking')
board.print()

board2 = SudokuBoard(1)
board2.print()
board2.solve('forwardchecking')
board2.print()



"""
||========================||
|| x | x | x || x | x | x ||
|| x | x | x || x | x | x ||
|| x | x | x || x | x | x ||
||========================||
|| x | x | x || x | x | x ||
|| x | x | x || x | x | x ||
|| x | x | x || x | x | x ||
||========================||
|| x | x | x || x | x | x ||
|| x | x | x || x | x | x ||
|| x | x | x || x | x | x ||
||========================||
"""

#Forward Checking:
#1.Create dictionary for each empty cell coordinate with value equal to possible domain
#2.Assign value to a chosen cell from its domain.
#3.Update the domains of all other cells
#4.If there is a cell with an empty domain, reset the most recently assigned cell