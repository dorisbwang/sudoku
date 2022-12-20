from cmu_cs3_graphics import *
from screenfunctions import *
import math
from stateclass import State
import random
import os
from backtracker import *

def modes_onScreenStart(app):
    # level
    app.lvlRows = 5
    app.lvlCols = 1
    app.lvlWidth = 200
    app.lvlHeight = 250
    app.lvlTop = 125
    app.lvlLeft = 50
    app.cellBorderWidth = 1
    app.lvlLabels = ['easy', 'medium', 'hard', 'expert', 'evil']
    app.currLvlCell = None
    app.lvlColor = [None for i in range(5)]
    app.fil = None
    app.mod = 'standard'

    # keyboard/mouse
    app.modeRows = 3
    app.modeTop = 125
    app.modeLeft = 400
    app.modeLabels = ['standard', 'mouse only', 'keyboard only']
    app.currModeCell = None
    app.modeColor = [None for i in range(3)]

    # start button
    app.butWidth = 150
    app.butHeight = 60
    app.butTop = 395
    app.butLeft = 250

    app.compMode = False
    
def modes_redrawAll(app):
    # titles levels
    drawBackground(app)
    drawLabel('LEVELS', 150, 75, size = 25, bold = True, align = 'center')
    drawLabel('select a level', 150, 105, align = 'center')

    # titles modes
    drawLabel('MODES', 500, 75, size = 25, bold = True, align = 'center')
    drawLabel('select a mode', 500, 105, align = 'center')

    drawLvl(app)
    drawLvlBorder(app)
    drawLvlLabels(app)

    drawMode(app)
    drawModeBorder(app)
    drawModeLabels(app)

    drawLabel('Press c and start for competition mode', 325, 470, align = 'center')
    drawRect(app.butLeft, app.butTop, app.butWidth, app.butHeight, fill = 'lightsteelblue', border = 'black')
    drawLabel('START', 325, 425, size = 20, align = 'center')

def modes_onMousePress(app, mouseX, mouseY):
    if getCellLvl(app, mouseX, mouseY) != None:
        app.fil = app.lvlLabels[getCellLvl(app, mouseX, mouseY)]
        for row in range(5):
            if app.currLvlCell == row:
                app.lvlColor[row] = 'lightsteelblue'
            else:
                app.lvlColor[row] = None
    elif getCellMode(app, mouseX, mouseY) != None:
        app.mod = app.modeLabels[getCellMode(app, mouseX, mouseY)]
        for row in range(3):
            if app.currModeCell == row:
                app.modeColor[row] = 'lightsteelblue'
            else:
                app.modeColor[row] = None
    elif (app.butLeft <= mouseX <= app.butLeft + app.butWidth and
        app.butTop <= mouseY <= app.butTop + app.butHeight):
        board = loadRandomBoard(app, app.fil)
        solution = solveSudoku(copy.deepcopy(board))
        print('solution!!', solution)
        app.state = State(board)
        app.state.solution = solution
        print(app.state.solution)
        setAuto(app)
        setActiveScreen('player')

def modes_onKeyPress(app, key):
    if key == 'c':
        app.fil = 'contest'
        app.compMode = True

def setAuto(app):
    if app.fil == 'easy':
        app.state.autoCand = False
    else:
        app.state.autoCand = True

def readFile(path):
    with open(path, "rt") as f:
        return f.read()

def makeBoardIntoList(stringBoard):
    list1DBoard = stringBoard.splitlines()
    board = []
    for item in list1DBoard:
        item = item.split(' ')
        board.append(item)
    for row in range(9):
        for col in range(9):
            board[row][col] = int(board[row][col])
    return board

def loadBoardPaths(filters):
    boardPaths = [ ]
    for filename in os.listdir(f'boards/'):
        if filename.endswith('.txt'):
            if hasFilters(filename, filters):
                boardPaths.append(f'boards/{filename}')
    return boardPaths

def hasFilters(filename, filters=None):
    if filters == None: return True
    for filter in filters:
        if filter not in filename:
            return False
    return True

def loadRandomBoard(app, filters=None):
    boardsPaths = loadBoardPaths(filters)
    finalPath = random.choice(boardsPaths)
    assignRandomLevel(app, finalPath)
    stringBoard = readFile(finalPath)
    board = makeBoardIntoList(stringBoard)
    return makeBoardIntoList(stringBoard)

def assignRandomLevel(app, finalPath):
    if 'easy' in finalPath:
        app.fil = 'easy'
    elif 'medium' in finalPath:
        app.fil = 'medium'
    elif 'hard' in finalPath:
        app.fil = 'hard'
    elif 'expert' in 'expert':
        app.fil = 'expert'
    else:
        app.fil = 'evil'

def getCellLvl(app, x, y):
    dx = x - app.lvlLeft
    dy = y - app.lvlTop
    cellWidth, cellHeight = getCellSize(app)
    row = math.floor(dy / cellHeight)
    col = math.floor(dx / cellWidth)
    if (0 <= row < app.lvlRows) and (0 <= col < app.lvlCols):
        app.currLvlCell = row
        return row

def getCellMode(app, x, y):
    dx = x - app.modeLeft
    dy = y - app.modeTop
    cellWidth, cellHeight = getCellModeSize(app)
    row = math.floor(dy / cellHeight)
    col = math.floor(dx / cellWidth)
    if (0 <= row < app.modeRows) and (0 <= col < app.lvlCols):
        app.currModeCell = row
        return row

def drawLvlLabels(app):
    cellWidth, cellHeight = getCellSize(app)
    for i in range(5):
        drawLabel(app.lvlLabels[i], app.lvlLeft + (app.lvlWidth / 2), 
                app.lvlTop + (cellHeight / 2) + (i * cellHeight), size = 16)

def drawModeLabels(app):
    cellWidth, cellHeight = getCellModeSize(app)
    for i in range(3):
        drawLabel(app.modeLabels[i], app.modeLeft + (app.lvlWidth / 2), 
                app.modeTop + (cellHeight / 2) + (i * cellHeight), size = 16)   

def drawLvl(app):
    for row in range(app.lvlRows):
        for col in range(app.lvlCols):
            if app.currLvlCell != None:
                color = app.lvlColor[row]
            else:
                color = None
            drawCell(app, row, col, color)

def drawMode(app):
    for row in range(app.modeRows):
        for col in range(app.lvlCols):
            if app.currModeCell != None:
                color = app.modeColor[row]
            else:
                color = None
            drawModeCell(app, row, col, color)

def drawLvlBorder(app):
  # draw the board outline (with double-thickness):
  drawRect(app.lvlLeft, app.lvlTop, app.lvlWidth, app.lvlHeight,
           fill=None, border='black',
           borderWidth=2*app.cellBorderWidth)

def drawModeBorder(app):
  # draw the board outline (with double-thickness):
  drawRect(app.modeLeft, app.modeTop, app.lvlWidth, app.lvlHeight,
           fill=None, border='black',
           borderWidth=2*app.cellBorderWidth)

def drawCell(app, row, col, color):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    drawRect(cellLeft, cellTop, cellWidth, cellHeight,
             fill=color, border='black',
             borderWidth=app.cellBorderWidth)

def drawModeCell(app, row, col, color):
    cellLeft, cellTop = getCellModeLeftTop(app, row, col)
    cellWidth, cellHeight = getCellModeSize(app)
    drawRect(cellLeft, cellTop, cellWidth, cellHeight,
             fill=color, border='black',
             borderWidth=app.cellBorderWidth)

def getCellLeftTop(app, row, col):
    cellWidth, cellHeight = getCellSize(app)
    cellLeft = app.lvlLeft + col * cellWidth
    cellTop = app.lvlTop + row * cellHeight
    return (cellLeft, cellTop)

def getCellModeLeftTop(app, row, col):
    cellWidth, cellHeight = getCellModeSize(app)
    cellLeft = app.modeLeft + col * cellWidth
    cellTop = app.modeTop + row * cellHeight
    return (cellLeft, cellTop)

def getCellSize(app):
    cellWidth = app.lvlWidth / app.lvlCols
    cellHeight = app.lvlHeight / app.lvlRows
    return (cellWidth, cellHeight)

def getCellModeSize(app):
    cellWidth = app.lvlWidth / app.lvlCols
    cellHeight = app.lvlHeight / 3
    return (cellWidth, cellHeight)

def drawBackground(app):
    drawRect(0, 0, 650, 500, fill = 'floralwhite')

# def main():
#     runAppWithScreens(initialScreen = 'modes', width = 650, height = 500)

# main()