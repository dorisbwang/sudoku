from cmu_cs3_graphics import *
from screenfunctions import *
from stateclass import State
import math
import os
import random
from modes import *
import copy

# draw/get board and keypad functions modified from CS3

def building_onScreenStart(app):
    # models for the sudoku board
    app.buildRows = 9
    app.buildCols = 9
    app.boardLeftBuild = 50
    app.boardTopBuild = 75
    app.boardWidthBuild = 360
    app.boardHeightBuild = 360
    app.cellBorderWidthBuild = 1
    app.cellSizeBuild = app.boardWidthBuild/app.buildRows
    app.whichBoard = [[0 for i in range(9)] for i in range(9)]
    app.boardColorBuild = startBoardColorsBuild(app)
    app.currBoardCellBuild = (0, 0)

    # models for the keyboard
    app.keypadRowsBuild = 3
    app.keypadColsBuild = 3
    app.keypadLeftBuild = 455
    app.keypadTopBuild = 130
    app.keypadWidthBuild = 150
    app.keypadHeightBuild = 150
    app.keypadCellBorderWidthBuild = 1 
    app.keypadCellSizeBuild = app.keypadWidthBuild/app.keypadRowsBuild
    app.keypadNumBuild = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    app.keypadColorsBuild = [([None] * app.keypadColsBuild) for row in range(app.keypadRowsBuild)]
    app.currKeypadCellBuild = None

def building_redrawAll(app):
    drawBackground(app)
    highlightBoardCellBuild(app)

    drawLabel('Sudoku', 50, 35, size=20, align = 'left', bold = True)
    drawLabel(f'Board Cell: {app.currBoardCellBuild}, Keypad Cell: {app.currKeypadCellBuild}',
                50, 60, size = 14, align = 'left')

    # board
    drawBoardBuild(app)
    drawBoardBorderBuild(app)
    drawBlockBorderBuild(app)
    drawBoardNumBuild(app)
    
    # keypad
    drawKeypadBuild(app)
    drawKeypadBorderBuild(app)

    drawLockButton(app)

def drawLockButton(app):
    color = 'pink'
    drawRect(455, 295, 150, 40, fill = color, border = 'black')
    drawLabel(f'Lock Board & Start Playing', 455 + 75, 315)

def getLock(app, mouseX, mouseY):
    if 455 <= mouseX <= 455 + 150 and 295 <= mouseY <= 295 + 40:
        app.state = State(app.whichBoard)
        solution = solveSudoku(copy.deepcopy(app.whichBoard))
        app.state.solution = solution
        setActiveScreen('player')

def building_onMousePress(app, mouseX, mouseY):
    getLock(app, mouseX, mouseY)
    # inside the sudoku board, get (row, col)
    if isMouseInBoardBuild(app, mouseX, mouseY):
        app.currBoardCellBuild = getCellBoardBuild(app, mouseX, mouseY)        

    # inside the number assignment board, get (row, col)
    if isMouseInKeypadBuild(app, mouseX, mouseY):
        app.currKeypadCellBuild = getCellKeypadBuild(app, mouseX, mouseY)
        value = getKeypadNumBuild(app)
            # adding value to the board
        if app.currBoardCellBuild != None:
            row, col = app.currBoardCellBuild
            existingVal = app.whichBoard[row][col]
            app.whichBoard[row][col] = value
            # if there's an existing value and autocand, unban that value
            if existingVal != 0:
                app.whichBoard[row][col] = 0
            # add the new value
        highlightKeypadCellBuild(app)

def building_onKeyPress(app, key):
    row, col = app.currBoardCellBuild
    existingVal = app.app.whichBoard[row][col]

    keyCellBuildSelection(app, key, row, col)

    # entering a number
    if app.whichBoard[row][col] == 0:
        value = getKeyValueBuild(app, key)
        if value > 0:
            if app.currBoardCellBuild != None:
                row, col = app.currBoardCellBuild
                existingVal = app.whichBoard[row][col]
                # if there's an existing value and autocand, unban that value
                if existingVal != 0:
                    app.whichBoard[row][col] = 0
                # add the new value
                app.whichBoard[row][col] = value


def getKeyValueBuild(app, key):
    value = 0
    if key == '1':
        value = 1
    elif key == '2':
        value = 2
    elif key == '3':
        value = 3
    elif key == '4':
        value = 4
    elif key == '5':
        value = 5
    elif key == '6':
        value = 6
    elif key == '7':
        value = 7
    elif key == '8':
        value = 8
    elif key == '9':
        value = 9
    return value

def keyCellBuildSelection(app, key, row, col):
    # cell selection
    if key == 'up':
        if 1 <= row <= 8:
            app.currBoardCellBuild = (row - 1, col)
    elif key == 'down':
        if 0 <= row <= 7:
            app.currBoardCellBuild = (row + 1, col)
    elif key == 'right':
        if 0 <= col <= 7:
            app.currBoardCellBuild = (row, col + 1)
    elif key == 'left':
        if 1 <= col <= 8:
            app.currBoardCellBuild = (row, col - 1)

def building_onMouseRelease(app, mouseX, mouseY):
     app.keypadColorsBuild = [([None] * app.keypadColsBuild) for row in range(app.keypadRowsBuild)]

def getKeypadNumBuild(app):
    keyrow, keycol = app.currKeypadCellBuild
    number = app.keypadNumBuild[keyrow][keycol]
    return number

def highlightKeypadCellBuild(app):
    if app.currKeypadCellBuild != None:
        currRow, currCol = app.currKeypadCellBuild
        for row in range(app.keypadRowsBuild):
            for col in range(app.keypadColsBuild):
                if currRow != row or currCol != col:
                     app.keypadColorsBuild[row][col] = None
                else:
                     app.keypadColorsBuild[row][col] = 'lavender'

def highlightBoardCellBuild(app):
    if app.currBoardCellBuild != None:
        currRow, currCol = app.currBoardCellBuild
        for row in range(9):
            for col in range(9):
                if app.whichBoard[row][col] != 0:
                    app.boardColorBuild[row][col] = 'lightsteelblue'
                if app.boardColorBuild[row][col] == 'cornflowerblue':
                    if currRow != row or currCol != col:
                        app.boardColorBuild[row][col] = 'lightsteelblue'
                elif app.boardColorBuild[row][col] != 'lightsteelblue':
                    if currRow != row or currCol != col:
                        app.boardColorBuild[row][col] = None
                    else:
                        app.boardColorBuild[row][col] = 'pink'
                elif app.boardColorBuild[row][col] == 'lightsteelblue':
                    if currRow == row and currCol == col:
                        app.boardColorBuild[row][col] = 'cornflowerblue'
                    else:
                        app.boardColorBuild[row][col] = 'lightsteelblue'

def isMouseInBoardBuild(app, mouseX, mouseY):
    if (app.boardLeftBuild <= mouseX <= app.boardLeftBuild + app.boardWidthBuild and
        app.boardTopBuild <= mouseY <= app.boardTopBuild + app.boardHeightBuild):
        return True
    return False

def isMouseInKeypadBuild(app, mouseX, mouseY):
    if (app.keypadLeftBuild <= mouseX <= app.keypadLeftBuild + app.keypadWidthBuild and
        app.keypadTopBuild <= mouseY <= app.keypadTopBuild + app.keypadHeightBuild):
        return True
    return False
    
def getCellBoardBuild(app, x, y):
    dx = x - app.boardLeftBuild
    dy = y - app.boardTopBuild
    cellWidth, cellHeight = getCellSizeBuild(app)
    row = math.floor(dy / cellHeight)
    col = math.floor(dx / cellWidth)
    if (0 <= row < app.buildRows) and (0 <= col < app.buildCols):
        return (row, col)

def getCellKeypadBuild(app, x, y):
    dx = x - app.keypadLeftBuild
    dy = y - app.keypadTopBuild
    cellWidth, cellHeight = getKeypadCellSizeBuild(app)
    row = math.floor(dy / cellHeight)
    col = math.floor(dx / cellWidth)
    if (0 <= row < app.buildRows) and (0 <= col < app.buildCols):
        return (row, col)

# printing the app.whichBoard
def drawBoardNumBuild(app):
    for row in range(app.buildRows):
        for col in range(app.buildCols):
            if app.whichBoard[row][col] != 0:
                drawLabel(f'{app.whichBoard[row][col]}', app.boardLeftBuild + app.cellSizeBuild/2 + (col * app.cellSizeBuild),
                        app.boardTopBuild + app.cellSizeBuild/2 + (row * app.cellSizeBuild), size = 18)

# function for drawing board

def drawBoardBuild(app):
    for row in range(app.buildRows):
        for col in range(app.buildCols):
            color = app.boardColorBuild[row][col]
            drawCellBuild(app, row, col, color)

def drawBoardBorderBuild(app):
  # draw the board outline (with double-thickness):
  drawRect(app.boardLeftBuild, app.boardTopBuild, app.boardWidthBuild, app.boardHeightBuild,
           fill=None, border='black',
           borderWidth=2*app.cellBorderWidthBuild)

# borders for the 9 blocks
def drawBlockBorderBuild(app):
    for i in range(4):
        # vertical
        drawLine(app.boardLeftBuild + (app.cellSizeBuild* 3 * i), app.boardTopBuild, 
                app.boardLeftBuild + (app.cellSizeBuild* 3 * i), app.boardTopBuild + app.boardWidthBuild,
                fill = 'black', lineWidth = 3)
        # horizontal
        drawLine(app.boardLeftBuild, app.boardTopBuild + (app.cellSizeBuild* 3 * i), 
                app.boardLeftBuild + app.boardWidthBuild, app.boardTopBuild + (app.cellSizeBuild* 3 * i),
                fill = 'black', lineWidth = 3)
    
def drawCellBuild(app, row, col, color):
    cellLeft, cellTop = getCellLeftTopBuild(app, row, col)
    cellWidth, cellHeight = getCellSizeBuild(app)
    drawRect(cellLeft, cellTop, cellWidth, cellHeight,
             fill=color, border='dimGrey',
             borderWidth=app.cellBorderWidthBuild)

def getCellLeftTopBuild(app, row, col):
    cellWidth, cellHeight = getCellSizeBuild(app)
    cellLeft = app.boardLeftBuild + col * cellWidth
    cellTop = app.boardTopBuild + row * cellHeight
    return (cellLeft, cellTop)

def getCellSizeBuild(app):
    cellWidth = app.boardWidthBuild / app.buildCols
    cellHeight = app.boardHeightBuild / app.buildRows
    return (cellWidth, cellHeight)

# functions for keypad

def drawKeypadBuild(app):
    for row in range(app.keypadRowsBuild):
        for col in range(app.keypadColsBuild):
            color =  app.keypadColorsBuild[row][col]
            drawKeypadCellBuild(app, row, col, color)
    drawKeypadNumbersBuild(app)

def drawKeypadNumbersBuild(app):
    for row in range(app.keypadRowsBuild):
        for col in range(app.keypadColsBuild):
            drawLabel(f'{app.keypadNumBuild[row][col]}', app.keypadLeftBuild + app.keypadCellSizeBuild/2 + (col * app.keypadCellSizeBuild),
                    app.keypadTopBuild + app.keypadCellSizeBuild/2 + (row * app.keypadCellSizeBuild), size = 18, bold = True)

def drawKeypadCellBuild(app, row, col, color):
    cellLeft, cellTop = getKeypadCellLeftTopBuild(app, row, col)
    cellWidth, cellHeight = getKeypadCellSizeBuild(app)
    drawRect(cellLeft, cellTop, cellWidth, cellHeight,
             fill=color, border='lavender',
             borderWidth=app.cellBorderWidthBuild)

def getKeypadCellLeftTopBuild(app, row, col):
    cellWidth, cellHeight = getKeypadCellSizeBuild(app)
    cellLeft = app.keypadLeftBuild + col * cellWidth
    cellTop = app.keypadTopBuild + row * cellHeight
    return (cellLeft, cellTop)

def getKeypadCellSizeBuild(app):
    cellWidth = app.keypadWidthBuild / app.keypadColsBuild
    cellHeight = app.keypadHeightBuild / app.keypadRowsBuild
    return (cellWidth, cellHeight)

def drawKeypadBorderBuild(app):
    drawRect(app.keypadLeftBuild, app.keypadTopBuild, app.keypadWidthBuild, app.keypadHeightBuild,
            fill=None, border='black',
            borderWidth=2*app.cellBorderWidthBuild)

def startBoardColorsBuild(app):
    colorBoard = [([None] * app.buildCols) for row in range(app.buildRows)]
    for row in range(app.buildRows):
        for col in range(app.buildCols):
            if app.whichBoard[row][col] != 0:
                colorBoard[row][col] = 'lightsteelblue'
    return colorBoard

def drawBackground(app):
    drawRect(0, 0, 650, 500, fill = 'floralwhite')
