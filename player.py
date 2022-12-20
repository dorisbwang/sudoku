from cmu_cs3_graphics import *
from screenfunctions import *
from stateclass import State
import math
import os
import random
import copy
from modes import *
from building import * 
import itertools
from PIL import Image
import pyscreenshot

# draw/get board functions modified from CS3
# taking screenshots/saving as pdf functions from geeks for geeks
# writefile from Kozbie

def restart(app):
    # models for the sudoku board
    app.rows = 9
    app.cols = 9
    app.boardLeft = 50
    app.boardTop = 75
    app.boardWidth = 360
    app.boardHeight = 360
    app.cellBorderWidth = 1
    app.cellSize = app.boardWidth/app.rows
    app.currBoardCell = (0, 0)

    # models for the keyboard
    app.keypadRows = 3
    app.keypadCols = 3
    app.keypadLeft = 455
    app.keypadTop = 130
    app.keypadWidth = 150
    app.keypadHeight = 150
    app.keypadCellBorderWidth = 1 
    app.keypadCellSize = app.keypadWidth/app.keypadRows
    app.keypadNum = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    app.keypadColors = [([None] * app.keypadCols) for row in range(app.keypadRows)]
    app.currKeypadCell = None

    app.redoList = []
    app.undoList = []

    app.gameOver = False
    app.noHint = False
    app.noHintText = 'No more of this hint left!'
    app.counter = 0
    app.mousePress = 0

    app.hintLegals = None


#drawing the board
def player_onScreenStart(app):
    restart(app) 

def player_redrawAll(app):
    drawBackground(app)
    highlightBoardCell(app)
    checkLegals(app)

    drawLabel('Sudoku', 50, 35, size=20, align = 'left', bold = True)
    drawLabel(f'Level: {app.fil}', 50, 60, size = 14, align = 'left')

    # board
    drawBoard(app)
    drawBoardBorder(app)
    drawBlockBorder(app)
    drawBoardNum(app)
    drawLegals(app)
    drawIncorrect(app)

    # keypad
    drawKeypad(app)
    drawDeleteNum(app)
    drawKeypadBorder(app)
    
    drawToggle(app)
    drawAutoButton(app)

    drawUndoMove(app)
    drawRedoMove(app)

    drawBottomButtons(app)
    drawSave(app)
    drawHelp(app)
    drawRestart(app)

    if app.noHint == True:
        drawNoHint(app)

    if app.gameOver == True:
        contents = getBoardContents(app)
        writeFile('myboard.txt', contents)
        drawRect(325, 250, 200, 100, fill = 'pink', border = 'black', align = 'center')
        drawLabel('YOU WIN!', 325, 250, size = 30)

def player_onStep(app):
    if app.noHint:
        app.counter += 1
        if app.counter == 25:
            app.noHint = False
    else:
        app.counter = 0

def getBoardContents(app):
    content = ''
    for row in range(9):
        contentL = ''
        for col in range(9):
            contentL += str(app.state.board[row][col]) + ' '
        contentL.strip()
        content += contentL + '\n'
    return content

def writeFile(path, contents):
    with open(path, "wt") as f:
        f.write(contents)

def readFile(path):
    with open(path, "rt") as f:
        return f.read()

def player_onMousePress(app, mouseX, mouseY):
    # taking a screenshot
    app.mousePress += 1
    if app.mousePress == 1:
        image = pyscreenshot.grab(bbox=(461,256, 858, 684))
        image.save("startboard.png")

    # restart and help button
    getRestart(app, mouseX, mouseY)
    getHelp(app, mouseX, mouseY)

    if app.gameOver == False:
        if app.mod != 'keyboard only':
            getToggle(app, mouseX, mouseY)
            getAuto(app, mouseX, mouseY)
            getUndoRedo(app, mouseX, mouseY)
            getDeleteNum(app, mouseX, mouseY)
            if not app.compMode:
                getBottomButtons(app, mouseX, mouseY)
            getSave(app, mouseX, mouseY)
            getHelp(app, mouseX, mouseY)

            # inside the sudoku board, get (row, col)
            if isMouseInBoard(app, mouseX, mouseY):
                app.currBoardCell = getCellBoard(app, mouseX, mouseY)  

            # inside the number assignment board, get (row, col)
            if isMouseInKeypad(app, mouseX, mouseY):
                app.currKeypadCell = getCellKeypad(app, mouseX, mouseY)
                value = getKeypadNum(app)
                row, col = app.currBoardCell
                existingVal = app.state.board[row][col]
                
                # if a board cell is selected
                if app.currBoardCell != None:
                    # normal mode
                    if app.state.normMode == True:
                        playNormal(app, row, col, existingVal, value)

                    # candidate mode
                    elif app.state.normMode == False :
                        playCand(app, row, col, existingVal, value)
                highlightKeypadCell(app)
        highlightBoardCell(app)

    # check if gameover with legals and incorrects
    if boardCorrect(app):
        app.gameOver = True


def playNormal(app, row, col, existingVal, value):
    # on the very first move, also append the og board and legals onto the undoList
    firstUndo(app)

    # adding value to the board, if same as on board, delete, else, set
    if app.state.ogboard[row][col] == 0:
        app.state.board[row][col] = 0

        # resets the legals of that cell after value removed
        app.state.legals[row][col] = copy.deepcopy(app.state.lastLegals[row][col]) # resets the cell to last legals
        cellRegions = app.state.getCellRegions(row, col)
        for region in cellRegions:
            for r, c in region:
                toDiscard = app.state.board[r][c] # bans new changes from the cell
                app.state.legals[row][col].discard(toDiscard)

        app.state.unban(row, col, value)

        if existingVal != value:
            app.state.unban(row, col, existingVal)
            app.state.set(row, col, value)

    # adding the new state to the undo list
    newUndo(app)

def firstUndo(app):
    if app.undoList == []:
        newState = (copy.deepcopy(app.state.board), copy.deepcopy(app.state.legals), copy.deepcopy(app.state.colorBoard))
        app.undoList.append(newState)

def newUndo(app):
    newState = (copy.deepcopy(app.state.board), copy.deepcopy(app.state.legals), copy.deepcopy(app.state.colorBoard))
    app.undoList.append(newState)
    app.redoList = []

def playCand(app, row, col, existingVal, value):
    # on the very first move, also append the og board and legals onto the undoList
    firstUndo(app)

    if app.state.ogboard[row][col] == 0:
        if app.state.autoCand == True:
            if value in app.state.legals[row][col]:
                app.state.legals[row][col].remove(value)
            else:
                app.state.legals[row][col].add(value)
            app.state.lastLegals[row][col] = copy.deepcopy(app.state.legals[row][col])
        else:
            if existingVal == 0:
                if value in app.state.manualLegals[row][col]:
                    app.state.manualLegals[row][col].remove(value)
                else:
                    app.state.manualLegals[row][col].add(value)

    # app.state.lastLegals[row][col] = copy.deepcopy(app.state.legals[row][col])
     
    # adding the new state to the undo list
    newUndo(app)

def undoMove(app):
    if len(app.undoList) > 1:
        lastBoard = app.undoList.pop(-1)
        app.redoList.append(lastBoard)
        currBoard = app.undoList[-1]
        app.state.board, app.state.legals, app.state.colorBoard = copy.deepcopy(currBoard[0]), copy.deepcopy(currBoard[1]), copy.deepcopy(currBoard[2])

def redoMove(app):
    if app.redoList != []:
        lastBoard = app.redoList.pop(-1)
        app.undoList.append(lastBoard)
        currBoard = app.undoList[-1]
        app.state.board, app.state.legals, app.state.colorBoard = copy.deepcopy(currBoard[0]), copy.deepcopy(currBoard[1]), copy.deepcopy(currBoard[2])
        if app.state.autoCand == True:
            for row in range(9):
                for col in range(9):
                    value = app.state.board[row][col]
                    if value != 0:
                        app.state.ban(row, col, value)


def player_onKeyPress(app, key):
    app.mousePress += 1
    if app.mousePress == 1:
        image = pyscreenshot.grab(bbox=(461,256, 858, 684))
        image.save("startboard.png")

    # help screen and restart
    if key == 'p':
        showHelp()
    if key == 't':
        showRestart()

    if app.gameOver == False:
        if app.mod != 'mouse only':

            row, col = app.currBoardCell
            existingVal = app.state.board[row][col]

            # cell selection
            keyCellSelection(app, key, row, col)
            if not app.compMode:
                keyHints(app, key)
            keyButtons(app, key)
            getToggleColor(app)

            # entering a number
            if app.state.ogboard[row][col] == 0:
                value = getKeyValue(app, key)
                if value > 0:
                    if app.state.normMode == True:
                        playNormal(app, row, col, existingVal, value)
                    elif app.state.normMode == False:
                        playCand(app, row, col, existingVal, value) 
        highlightBoardCell(app)
    
    # check if gameover with legals and incorrects
    if boardCorrect(app):
        app.gameOver = True
        

def getKeyValue(app, key):
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

def keyCellSelection(app, key, row, col):
    # cell selection
    if key == 'up':
        if 1 <= row <= 8:
            app.currBoardCell = (row - 1, col)
    elif key == 'down':
        if 0 <= row <= 7:
            app.currBoardCell = (row + 1, col)
    elif key == 'right':
        if 0 <= col <= 7:
            app.currBoardCell = (row, col + 1)
    elif key == 'left':
        if 1 <= col <= 8:
            app.currBoardCell = (row, col - 1)

def keyButtons(app, key):
    if key == 'a':
        app.state.autoCand = not app.state.autoCand
        if app.state.autoCand == True:
            for row in range(9):
                for col in range(9):
                    value = app.state.board[row][col]
                    if value != 0:
                        app.state.ban(row, col, value)
    if key == 'n':
        app.state.normMode = True 
    if key == 'c':  
        app.state.normMode = False
    if key == 'backspace':
        deleteNum(app)
    if key == 'u':
        undoMove(app)
    if key == 'r':
        redoMove(app)
    if key == 'b':
        savePDF(app)
        
    getToggleColor(app)

def keyHints(app, key):
    # play singleton
    if key == 's':
        showSingles(app)
    # play all singletons
    if key == 'S':
        playSingles(app)
    if key == 'A':
        playAllSingles(app)
    if key == 'h':
        showHint2(app)
    if key == 'H':
        doHint2(app)

def playSingles(app):
    if app.fil == 'medium' or app.fil == 'hard' or app.fil == 'expert' or app.fil == 'evil':
        # if the very first move, also append the og board and legals onto the undoList
        firstUndo(app)
        singles = 0
        stop = False
        for row in range(9):
            if stop: break
            for col in range(9):
                legals = list(app.state.legals[row][col])
                if len(legals) == 1:
                    app.currBoardCell = (row, col)
                    app.state.set(row, col, legals[0])
                    singles += 1
                    stop = True
                    break
        if singles == 0:
            app.noHint = True
        else:
            newUndo(app)

def showSingles(app):
    if app.fil == 'medium' or app.fil == 'hard' or app.fil == 'expert' or app.fil == 'evil':
        # if the very first move, also append the og board and legals onto the undoList
        firstUndo(app)
        singles = 0
        stop = False
        for row in range(9):
            if stop: break
            for col in range(9):
                legals = list(app.state.legals[row][col])
                if len(legals) == 1:
                    app.state.colorBoard[row][col] = 'lightgreen'
                    singles += 1
                    stop = True
                    break
        if singles == 0:
            app.noHint = True
        else:
            newUndo(app)

def playAllSingles(app):
    if app.fil == 'medium' or app.fil == 'hard' or app.fil == 'expert' or app.fil == 'evil':
        # if the very first move, also append the og board and legals onto the undoList
        if app.undoList == []:
            newState = (copy.deepcopy(app.state.board), copy.deepcopy(app.state.legals), copy.deepcopy(app.state.colorBoard))
            app.undoList.append(newState)
        singles = 0
        for row in range(9):
            for col in range(9):
                legals = list(app.state.legals[row][col])
                if len(legals) == 1:
                    app.currBoardCell = (row, col)
                    app.state.set(row, col, legals[0])
                    singles += 1
        if singles == 0:
            app.noHint = True
        else:
            newState = (copy.deepcopy(app.state.board), copy.deepcopy(app.state.legals), copy.deepcopy(app.state.colorBoard))
            app.undoList.append(newState)
            app.redoList = []
'''
THIS IS HINT 2 !!!!!!!!!!!!!
'''
def isValidTuples(app, combination, n):
    legalsSet = set()
    for row, col in combination:
        if app.state.legals[row][col] == set():
            return False
        legalsSet = legalsSet.union(app.state.legals[row][col])
    if len(legalsSet) == n:
        return True
    return False

def getValidLegals(app, combination, n):
    legalsSet = set()
    for row, col in combination:
        legalsSet = legalsSet.union(app.state.legals[row][col])
    return legalsSet

def doHint2(app):
    if app.fil != 'easy':
        stop = False
        hintCount = 0
        firstUndo(app)
        for n in range(2, 6):
            if stop:
                break
            # n is amount of unique numbers for n cells
            allRegions = app.state.getAllRegions() # list of regions [[rowRegions], [colRegions], [blockRegions]]
            for region in allRegions:
                if stop:
                    break
                # the region of lists of 9 tuples, for each region, check each combination of n cells 
                combinationList = list(itertools.combinations(region, n))

                for combination in combinationList: # a tuple of n cells
                # get n tuples with n unique legals
                    if isValidTuples(app, combination, n):
                        validCombo = combination # tuple of cells
                        validLegals = getValidLegals(app, combination, n)
                        comboRegions = app.state.getAllRegionsThatContainTargets(validCombo) 
                        before = copy.deepcopy(app.state.legals)
                        for comboRegion in comboRegions:
                            for r, c in comboRegion:
                                app.state.legals[r][c] = app.state.legals[r][c] - validLegals
                                for row, col in validCombo:
                                    app.state.legals[row][col] = before[row][col]
                        after = copy.deepcopy(app.state.legals)

                        if after != before:
                            stop = True
                            hintCount += 1
                            break
        if hintCount == 0:
            app.noHint = True
        newUndo(app)      

def showHint2(app):
    if app.fil != 'easy':
        stop = False
        hintCount = 0
        firstUndo(app)
        for n in range(2, 6):
            if stop:
                break
            # n is amount of unique numbers for n cells
            allRegions = app.state.getAllRegions() # list of regions [[rowRegions], [colRegions], [blockRegions]]
            for region in allRegions:
                if stop:
                    break
                # a region of lists of 9 tuples, for each region, check each combination of n cells 
                combinationList = list(itertools.combinations(region, n))
                
                for combination in combinationList: # a tuple of n cells
                # get n tuples with n unique legals
                    if isValidTuples(app, combination, n):
                        validCombo = combination # tuple of cells
                        validLegals = getValidLegals(app, combination, n)
                        comboRegions = app.state.getAllRegionsThatContainTargets(validCombo) 
                        before = copy.deepcopy(app.state.legals)
                        for comboRegion in comboRegions:
                            for r, c in comboRegion:
                                app.state.legals[r][c] = app.state.legals[r][c] - validLegals
                                for row, col in validCombo:
                                    app.state.legals[row][col] = before[row][col]

                        after = copy.deepcopy(app.state.legals)
                        app.state.legals = before

                        if before == after:
                            for row, col in validCombo:
                                app.state.colorBoard[row][col] = 'blue'

                        elif before != after:
                            # for comboRegion in comboRegions:
                            #     for ro, co in comboRegion:
                            #         app.state.colorBoard[ro][co] = palegreen
                            #         # highlightBoardCell(app)
                            for row, col in validCombo:
                                app.state.colorBoard[row][col] = 'lightgreen'
                                # highlightBoardCell(app)

                            stop = True
                            hintCount += 1
                            break

        if hintCount == 0:
            app.noHint = True
        newUndo(app)      

# needs backtracker
def boardCorrect(app):
    if app.state.board == app.state.solution:
        return True
    return False

# needs backtracker
def checkLegals(app):
    if app.compMode == False:
        # check red dot
        # looping through self.legals
        for row in range(9):
            for col in range(9):
                if app.state.ogboard[row][col] == 0:
                    existingVal = app.state.board[row][col]
                    solutionVal = app.state.solution[row][col]
                    existingLegals = app.state.legals[row][col]
                    if (solutionVal not in existingLegals) and app.state.board[row][col] == 0:
                        app.state.incorrect[row][col] = 1
                        if app.compMode:
                            app.gameOver = True
                    elif (existingVal != solutionVal and existingVal != 0):
                        app.state.incorrect[row][col] = 1
                        if app.compMode:
                            app.gameOver = True
                    else:
                        app.state.incorrect[row][col] = 0
            

def player_onMouseRelease(app, mouseX, mouseY):
    app.keypadColors = [([None] * app.keypadCols) for row in range(app.keypadRows)]

def getKeypadNum(app):
    keyrow, keycol = app.currKeypadCell
    number = app.keypadNum[keyrow][keycol]
    return number

def highlightKeypadCell(app):
    if app.currKeypadCell != None:
        currRow, currCol = app.currKeypadCell
        for row in range(app.keypadRows):
            for col in range(app.keypadCols):
                if currRow != row or currCol != col:
                    app.keypadColors[row][col] = None
                else:
                    app.keypadColors[row][col] = 'lavender'

def highlightBoardCell(app):
    if app.currBoardCell != None:
        currRow, currCol = app.currBoardCell
        for row in range(9):
            for col in range(9):
                if app.state.colorBoard[row][col] == 'cornflowerblue':
                    if currRow != row or currCol != col:
                        app.state.colorBoard[row][col] = 'lightsteelblue'
                elif app.state.colorBoard[row][col] == 'lightgreen':
                    if app.state.board[row][col] != 0:
                            app.state.colorBoard[row][col] = None
                elif app.state.colorBoard[row][col] != 'lightsteelblue':
                    if currRow != row or currCol != col:
                        app.state.colorBoard[row][col] = None
                    else:
                        app.state.colorBoard[row][col] = 'pink'
                elif app.state.colorBoard[row][col] == 'lightsteelblue':
                    if currRow == row and currCol == col:
                        app.state.colorBoard[row][col] = 'cornflowerblue'
                    else:
                        app.state.colorBoard[row][col] = 'lightsteelblue'

def drawLegals(app):
    for row in range(9):
        for col in range(9):
            if app.state.board[row][col] == 0:
                drawLegalCell(app, row, col)
       
def drawLegalCell(app, row, col):
    if app.state.autoCand == True:
        legal = app.state.legals[row][col]
    else:
        legal = app.state.manualLegals[row][col]
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    x = app.cellSize / 6
    cellNum = 1
    for r in range(3):
        for c in range(3):
            if cellNum in legal:
                drawLabel(f'{cellNum}', cellLeft + x + c * 2 * x, 
                cellTop + x + r * 2 * x, fill = 'gray')
            cellNum += 1

# NEEDS WORK AFTER BT
def drawIncorrect(app):
    for row in range(9):
        for col in range(9):
            if app.state.incorrect[row][col] == 1:
                cellLeft, cellTop = getCellLeftTop(app, row, col)
                drawCircle(cellLeft + 30, cellTop + 30, 3, fill = 'red')

def isMouseInBoard(app, mouseX, mouseY):
    if (app.boardLeft <= mouseX <= app.boardLeft + app.boardWidth and
        app.boardTop <= mouseY <= app.boardTop + app.boardHeight):
        return True
    return False

def isMouseInKeypad(app, mouseX, mouseY):
    if (app.keypadLeft <= mouseX <= app.keypadLeft + app.keypadWidth and
        app.keypadTop <= mouseY <= app.keypadTop + app.keypadHeight):
        return True
    return False
    
def getCellBoard(app, x, y):
    dx = x - app.boardLeft
    dy = y - app.boardTop
    cellWidth, cellHeight = getCellSize(app)
    row = math.floor(dy / cellHeight)
    col = math.floor(dx / cellWidth)
    if (0 <= row < app.rows) and (0 <= col < app.cols):
        return (row, col)

def getCellKeypad(app, x, y):
    dx = x - app.keypadLeft
    dy = y - app.keypadTop
    cellWidth, cellHeight = getKeypadCellSize(app)
    row = math.floor(dy / cellHeight)
    col = math.floor(dx / cellWidth)
    if (0 <= row < app.rows) and (0 <= col < app.cols):
        return (row, col)

# make the cells with existing values be lightsteelblue
def startBoardColors(app):
    colorBoard = [([None] * app.cols) for row in range(app.rows)]
    for row in range(app.rows):
        for col in range(app.cols):
            if app.state.board[row][col] != 0:
                colorBoard[row][col] = 'lightsteelblue'
    return colorBoard

# make the board into a 2D list
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

# printing the app.state.board
def drawBoardNum(app):
    for row in range(app.rows):
        for col in range(app.cols):
            if app.state.board[row][col] != 0:
                drawLabel(f'{app.state.board[row][col]}', app.boardLeft + app.cellSize/2 + (col * app.cellSize),
                        app.boardTop + app.cellSize/2 + (row * app.cellSize), size = 18)

# function for drawing board

def drawBoard(app):
    for row in range(app.rows):
        for col in range(app.cols):
            color = app.state.colorBoard[row][col]
            drawCell(app, row, col, color)

def drawBoardBorder(app):
  # draw the board outline (with double-thickness):
  drawRect(app.boardLeft, app.boardTop, app.boardWidth, app.boardHeight,
           fill=None, border='black',
           borderWidth=2*app.cellBorderWidth)

# borders for the 9 blocks
def drawBlockBorder(app):
    for i in range(4):
        # vertical
        drawLine(app.boardLeft + (app.cellSize* 3 * i), app.boardTop, 
                app.boardLeft + (app.cellSize* 3 * i), app.boardTop + app.boardWidth,
                fill = 'black', lineWidth = 3)
        # horizontal
        drawLine(app.boardLeft, app.boardTop + (app.cellSize* 3 * i), 
                app.boardLeft + app.boardWidth, app.boardTop + (app.cellSize* 3 * i),
                fill = 'black', lineWidth = 3)
    
def drawCell(app, row, col, color):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    drawRect(cellLeft, cellTop, cellWidth, cellHeight,
             fill=color, border='dimGrey',
             borderWidth=app.cellBorderWidth)

def getCellLeftTop(app, row, col):
    cellWidth, cellHeight = getCellSize(app)
    cellLeft = app.boardLeft + col * cellWidth
    cellTop = app.boardTop + row * cellHeight
    return (cellLeft, cellTop)

def getCellSize(app):
    cellWidth = app.boardWidth / app.cols
    cellHeight = app.boardHeight / app.rows
    return (cellWidth, cellHeight)

'''
save board as pdf
'''
# from geeks for geeks, modified
def savePDF(app):
    image = pyscreenshot.grab(bbox=(461,256, 858, 684))
    
    # To view the screenshot
    image.show()
    
    # To save the screenshot
    image.save("endboard.png")

    image_1 = Image.open(r'startboard.png')
    image_2 = Image.open(r'endboard.png')

    im_1 = image_1.convert('RGB')
    im_2 = image_2.convert('RGB')

    image_list = [im_2]

    im_1.save(r'boards.pdf', save_all=True, append_images=image_list)


def drawSave(app):
    drawRect(280, 30, 130, 30, fill = 'lavenderblush', border = 'black', borderWidth = 1)
    drawLabel(f'Save Board as PDF', 280 + (130/2), 30 + 15, align = 'center')

def getSave(app, mouseX, mouseY):
    if 280 <= mouseX <= 280 + 130 and 30 <= mouseY <= 60:
        savePDF(app)

'''
draw help and restart
'''
def drawHelp(app):
    drawRect(455, 30, 60, 30, fill = 'lavender', border = 'black', borderWidth = 1)
    drawLabel(f'Help (p)', 455 + 30, 30 + 15, align = 'center')

def getHelp(app, mouseX, mouseY):
    if 455 <= mouseX <= 455 + 60 and 30 <= mouseY <= 30 + 30:
        showHelp()

def showHelp():
    setActiveScreen('help')

def drawRestart(app):
    drawRect(545, 30, 60, 30, fill = 'lavender', border = 'black', borderWidth = 1)
    drawLabel(f'Restart (t)', 545 + 30, 30 + 15, align = 'center')

def getRestart(app, mouseX, mouseY):
    if 545 <= mouseX <= 545 + 60 and 30 <= mouseY <= 60:
        showRestart()

def showRestart():
    setActiveScreen('splash')



"""
bottom row of buttons
['Show Singles (s)', 'Play Singles', 'Play All Singles', 'Show Hint 2', 'Play Hint 2']
"""

def drawBottomButtons(app):
    labels = ['Show Singles (s)', 'Play Singles (S)', 'Play All Singles (A)' , 'Show Hint 2 (h)', 'Play Hint 2 (H)']
    for i in range(5):
        drawRect(50 + 115 * i, 450, 100, 30, fill = 'lavenderblush', border = 'black', borderWidth = 1)
    for i in range(5):
        drawLabel(f'{labels[i]}', 100 + (115 * i), 450 + 15, align = 'center', size = 11)

def getBottomButtons(app, mouseX, mouseY):
    if 450 <= mouseY <= 450 + 100:
        if 50 + 115 * 0 <= mouseX <= 50 + 115 * 0 + 100:
            showSingles(app)
        elif 50 + 115 * 1 <= mouseX <= 50 + 115 * 1 + 100:
            playSingles(app)
        elif 50 + 115 * 2 <= mouseX <= 50 + 115 * 2 + 100:
            playAllSingles(app)
        elif 50 + 115 * 3 <= mouseX <= 50 + 115 * 3 + 100:
            showHint2(app)
        elif 50 + 115 * 4 <= mouseX <= 50 + 115 * 4 + 100:
            doHint2(app)

def drawNoHint(app):
    drawRect(325, 250, 250, 60, fill = 'white', border = 'red', align = 'center')
    drawLabel(app.noHintText, 325, 250, size = 18)

def drawUndoMove(app):
    drawRect(455, 390, 60, 30, fill = 'lavender', border = 'black')
    drawLabel(f'Undo (u)', 455 + 30, 390 + 15, align = 'center')

def drawRedoMove(app):
    drawRect(545, 390, 60, 30, fill = 'lavender', border = 'black')
    drawLabel(f'Redo (r)', 545 + 30, 390 + 15, align = 'center')

def getUndoRedo(app, mouseX, mouseY):
    if 390 <= mouseY <= 390 + 30:
        if 455 <= mouseX <= 455 + 60:
            undoMove(app)
        elif 545 <= mouseX <= 545 + 60:
            redoMove(app)

def drawDeleteNum(app):
    drawRect(455, 280, 150, 40, fill = 'lavender')
    drawLabel(f'X', 530, 280 + 20, size = 18, bold = True, align = 'center')

def getDeleteNum(app, mouseX, mouseY):
    if 455 <= mouseX <= 455 + 150 and 280 <= mouseY <= 280 + 40:
        deleteNum(app)

def deleteNum(app):
    row, col = app.currBoardCell
    existingVal = app.state.board[row][col]
    app.state.board[row][col] = 0

    # resets the legals of that cell after value removed
    app.state.legals[row][col] = copy.deepcopy(app.state.lastLegals[row][col]) # resets the cell to last legals
    cellRegions = app.state.getCellRegions(row, col)
    for region in cellRegions:
        for r, c in region:
            toDiscard = app.state.board[r][c] # bans new changes from the cell
            app.state.legals[row][col].discard(toDiscard)

    app.state.unban(row, col, existingVal)

def drawToggle(app):
    labels = ['Normal (n)', 'Candidate (c)']

    for i in range(2):
        drawRect(455 + i * 75, 75, 75, 40, fill = app.state.toggleLegal[i], border = 'black', borderWidth = 1)
        drawRect(455, 75, 150, 40, fill = None, border = 'black', borderWidth = 2)
        drawLabel(f'{labels[i]}', 455 + 75/2 + 75 * i, 95, align = 'center', size = 11)

def getToggle(app, mouseX, mouseY):
    if 75 <= mouseY <= 75 + 40:
        if 455 <= mouseX < 455 + 75:
            app.state.normMode = True

        elif 455 + 75 <= mouseX <= 455 + 150:
            app.state.normMode = False
    
    getToggleColor(app)

def getToggleColor(app):
    if app.state.normMode == False:
        app.state.toggleLegal = [None, 'pink']
    elif app.state.normMode == True:
        app.state.toggleLegal = ['pink', None]

def drawAutoButton(app):
    if app.state.autoCand == True:
        color = 'pink'
        toggle = 'On'
    else:
        color = None
        toggle = 'Off'
    drawRect(455, 335, 150, 40, fill = color, border = 'black')
    drawLabel(f'Auto Candidate: {toggle} (a)', 455 + 75, 335 + 20, align = 'center')

def getAuto(app, mouseX, mouseY):
    if 455 <= mouseX <= 455 + 150 and 335 <= mouseY <= 335 + 40:
        app.state.autoCand = not app.state.autoCand
        if app.state.autoCand == True:
            for row in range(9):
                for col in range(9):
                    value = app.state.board[row][col]
                    if value != 0:
                        app.state.ban(row, col, value)

# functions for keypad

def drawKeypad(app):
    for row in range(app.keypadRows):
        for col in range(app.keypadCols):
            color = app.keypadColors[row][col]
            drawKeypadCell(app, row, col, color)
    drawKeypadNumbers(app)

def drawKeypadNumbers(app):
    for row in range(app.keypadRows):
        for col in range(app.keypadCols):
            drawLabel(f'{app.keypadNum[row][col]}', app.keypadLeft + app.keypadCellSize/2 + (col * app.keypadCellSize),
                    app.keypadTop + app.keypadCellSize/2 + (row * app.keypadCellSize), size = 18, bold = True)

def drawKeypadCell(app, row, col, color):
    cellLeft, cellTop = getKeypadCellLeftTop(app, row, col)
    cellWidth, cellHeight = getKeypadCellSize(app)
    drawRect(cellLeft, cellTop, cellWidth, cellHeight,
             fill=color, border='lavender',
             borderWidth=app.cellBorderWidth)

def getKeypadCellLeftTop(app, row, col):
    cellWidth, cellHeight = getKeypadCellSize(app)
    cellLeft = app.keypadLeft + col * cellWidth
    cellTop = app.keypadTop + row * cellHeight
    return (cellLeft, cellTop)

def getKeypadCellSize(app):
    cellWidth = app.keypadWidth / app.keypadCols
    cellHeight = app.keypadHeight / app.keypadRows
    return (cellWidth, cellHeight)

def drawKeypadBorder(app):
    drawRect(app.keypadLeft, app.keypadTop, app.keypadWidth, app.keypadHeight + 40,
            fill=None, border='black',
            borderWidth=2*app.cellBorderWidth)

def drawBackground(app):
    drawRect(0, 0, 650, 500, fill = 'floralwhite')

# def main():
#     runAppWithScreens(initialScreen = 'player', width = 650, height = 500)

# main()
