from cmu_cs3_graphics import *
from screenfunctions import *
import math
from stateclass import State
import random
import os
import copy

def solveSudoku(board):
    currState = State(board)
    for row in range(9):
        for col in range(9):
            if currState.board[row][col] != 0:
                currState.setbacktrack(row, col, currState.board[row][col])
    zerosList = zeroCells(board, currState)
    return solver(currState, zerosList)
    
def zeroCells(board, currState):
    result = []
    for row in range(len(board)):
        for col in range(len(board[0])):
            if currState.board[row][col] == 0:
                result.append((row,col))
    return result

def legalsGone(currState):
    for row in range(9):
        for col in range(9):
            if currState.legals[row][col] != set():
                return False
    return True

def solver(currState, zerosList):
    # print(currState.printBoard())
    # print(currState.printLegals())
    if legalsGone(currState):
        return currState.board
    else:
        leastLegals = 9
        leastLegalsCell = None
        leastLegalsIndex = None
        for cellInd in range(len(zerosList)):
            # getting the cell with the least legals
            row, col = zerosList[cellInd]
            if len(currState.legals[row][col]) < leastLegals:
                leastLegalsCell = (row, col)
                leastLegals = len(currState.legals[row][col])
                leastLegalsIndex = cellInd

        # testing each legal
        row, col = leastLegalsCell
        legals = copy.deepcopy(currState.legals[row][col])
        for testNum in legals:
            if isLegal(testNum, currState, row, col):
                # currState.board[row][col] = testNum
                lastBoard = copy.deepcopy(currState.board)
                lastLegals = copy.deepcopy(currState.legals)
                currState.setbacktrack(row, col, testNum)
                restZeros = copy.deepcopy(zerosList)
                restZeros.pop(leastLegalsIndex)
                updatedBoard = solver(currState, restZeros)
                if updatedBoard != None:
                    return updatedBoard
                currState.board = copy.deepcopy(lastBoard)
                currState.legals = copy.deepcopy(lastLegals)

        return None
    
def isLegal(testNum, currState, r, c):
    rowRegionVals = currState.getRowRegionValues(r)
    colRegionVals = currState.getColRegionValues(c)
    blockRegionVals = currState.getBlockRegionValues(r, c)

    if testNum in rowRegionVals or testNum in colRegionVals or testNum in blockRegionVals:
        return False

    return True

# print('printing the final', solveSudoku(board))

    
   