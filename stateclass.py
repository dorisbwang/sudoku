from cmu_cs3_graphics import *
from screenfunctions import *
import math
import copy

# general outline taken from Kozbie's hints with some modifications
# print functions from Kozbie's hints

class State():
    def __init__(self, board):
        self.board = board  # the actual board that will be displayed
        self.ogboard = copy.deepcopy(board) # the og board, can't be manipulated
        self.legals = [[{1, 2, 3, 4, 5, 6, 7, 8, 9} for i in range(9)] for i in range(9)] # the blank board legals
        self.lastLegals = copy.deepcopy(self.legals)
        self.manualLegals = [[{0, 0, 0, 0, 0, 0, 0, 0, 0} for i in range(9)] for i in range(9)]
        self.colorBoard = [([None] * 9) for row in range(9)]
        self.startBoardColors()

        self.incorrect = [[0 for i in range (9)] for i in range(9)]
        self.keyboardMode = True
        self.mouseMode = True
        self.filters = []
        self.autoCand = False
        self.normMode = True
        self.toggleLegal = ['pink', None]
        self.solution = None

        for row in range(9):
            for col in range(9):
                value = self.board[row][col]
                if value != 0:
                    self.ban(row, col, value)

    def setbacktrack(self, row, col, value):
        self.board[row][col] = value
        self.legals[row][col] = set()
        cellRegions = self.getCellRegions(row, col)

        for region in cellRegions:
                for r, c in region:
                    self.legals[r][c].discard(value)

    def set(self, row, col, value):
        if self.ogboard[row][col] == 0:
            self.board[row][col] = value
            self.ban(row, col, value)

    def ban(self, row, col, values):
        cellRegions = self.getCellRegions(row, col)

        # adds the previous legals into lastLegals whenever banning happens
        self.lastLegals[row][col] = copy.deepcopy(self.legals[row][col])
        self.legals[row][col] = set()

        if isinstance(values, int):
            for region in cellRegions:
                for r, c in region:
                    self.legals[r][c].discard(values)
        else:
            for value in values:
                for region in cellRegions:
                    for r, c in region:
                        self.legals[r][c].discard(value)
    
    def unban(self, row, col, values):
        cellRegions = self.getCellRegions(row, col)
        
        if isinstance(values, int):
            for region in cellRegions:
                for r, c in region:
                    self.legals[r][c].add(values)
        else:
            for region in cellRegions:
                for value in values:
                    for r, c in region:
                        self.legals[r][c].add(value)
        
        self.board[row][col] = 0
        # self.legals[row][col] = copy.deepcopy(self.lastLegals[row][col])
        self.legals = copy.deepcopy(self.lastLegals)

        for row in range(9):
            for col in range(9):
                value = self.board[row][col]
                if value != 0:
                    self.ban(row, col, value)


        # self.board[row][col] = 0
        # self.legals = [[{1, 2, 3, 4, 5, 6, 7, 8, 9} for i in range(9)] for i in range(9)]
        # for row in range(9):
        #     for col in range(9):
        #         value = self.board[row][col]
        #         if value != 0:
        #             self.ban(row, col, value)

    def startBoardColors(self):
        for row in range(9):
            for col in range(9):
                if self.ogboard[row][col] != 0:
                    self.colorBoard[row][col] = 'lightsteelblue'
        return self.colorBoard

    def getRowRegionValues(self, row):
        vals = set()
        rowRegion = self.getRowRegion(row)
        for r, c in rowRegion:
            vals.add(self.board[r][c])
        return vals

    def getColRegionValues(self, col):
        vals = set()
        colRegion = self.getColRegion(col)
        for r, c in colRegion:
            vals.add(self.board[r][c])
        return vals

    def getBlockRegionValues(self, row, col):
        vals = set()
        blockRegion = self.getBlockRegionByCell(row, col)
        for r, c in blockRegion:
            vals.add(self.board[r][c])
        return vals

    # done
    def getRowRegion(self, row):
        region = []
        for col in range(9):
            region.append((row, col))
        return region
    
    # done
    def getColRegion(self, col):
        region = []
        for row in range(9):
            region.append((row, col))
        return region

    # done
    def getBlockRegion(self, block):
        if block <= 2:
            s, e = 0, 3
        elif block <= 5:
            s, e = 3, 6
        else:
            s, e = 6, 9

        region = []
        for row in range(s, e):
            for i in range(3):
                col = i + 3 * (block % 3)
                region.append((row, col))
        return region
        
    # done
    def getBlock(self, row, col):
        if col // 3 == 0:
            start = 0
        elif col // 3 == 1:
            start = 1
        else:
            start = 2
        block = (row // 3) * 3 + start
        return block

    # done (?)
    def getBlockRegionByCell(self, row, col):
        block = self.getBlock(row, col)
        return self.getBlockRegion(block)

    # kinda confused? done
    def getCellRegions(self, row, col):
        # returns row region, col region, and block region?
        cellRegions = []

        cellRegions.append(self.getRowRegion(row))
        cellRegions.append(self.getColRegion(col))
        cellRegions.append(self.getBlockRegionByCell(row, col))

        return cellRegions
    
    # CONFUSED!!! done
    def getAllRegions(self):
        # ??? just not really sure why i need this
        # returns all row regions, col regions, and block regions?
        # return a 2D list of regions

        allRegions = []

        # rowsRegions
        for row in range(9):
            allRegions.append(self.getRowRegion(row))

        # colsRegion
        for col in range(9):
            allRegions.append(self.getColRegion(col))

        # blockRegion
        for block in range(9):
            allRegions.append(self.getBlockRegion(block))

        return allRegions

    # done ig??
    def getAllRegionsThatContainTargets(self, targets):
        # used in hint 2
        # targets as a list of tuples of target cells
        # use to ban the n unique values from the target regions

        # allRegions = []
        # targetNum = 0
        # for row, col in targets:
        #     allRegions.append(self.getCellRegions(row, col))
        #     targetNum += 1

        # print('allRegions', allRegions)


        # noDuplicateAllRegions = []
        # for region in allRegions:
        #     if region not in noDuplicateAllRegions:
        #         noDuplicateAllRegions.extend(region)
        
        # print(noDuplicateAllRegions)
        # return noDuplicateAllRegions



        startRow, startCol = targets[0]
        startBlock = self.getBlockRegionByCell(startRow, startCol)

        rowSame = True
        for row, col in targets:
            if row != startRow:
                rowSame = False

        colSame = True
        for row, col in targets:
            if col != startCol:
                colSame = False

        blockSame = True
        for row, col in targets:
            if self.getBlockRegionByCell(row, col) != startBlock:
                blockSame = False

        allRegions = []
        if rowSame == True:
            allRegions.append(self.getRowRegion(startRow))
        if colSame == True:
            allRegions.append(self.getColRegion(startCol))
        if blockSame == True:
            block = self.getBlockRegionByCell(startRow, startCol)
            allRegions.append(block)

        return allRegions

    def printBoard(self): 
        for row in range(9):
            cols = []
            for col in range(9):
                cols.append(self.board[row][col])
            print(cols)
            print()

    def printLegals(self):
        colWidth = 4
        for col in range(9):
            colWidth = max(colWidth, 1+max([len(self.legals[row][col]) for row in range(9)]))
        for row in range(9):
            for col in range(9):
                label = ''.join([str(v) for v in sorted(self.legals[row][col])])
                if label == '': label = '-'
                print(f"{' '*(colWidth - len(label))}{label}", end='')
            print()

    def print(self): 
        self.printBoard(); self.printLegals()

        
