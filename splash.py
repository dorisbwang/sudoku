from cmu_cs3_graphics import *
from screenfunctions import *
import math
from stateclass import State

def splash_onScreenStart(app):
    app.bWidth = 150
    app.bHeight = 60
    app.bTop = 275
    app.bLeft = 140

    app.mWidth = 150
    app.mHeight = 60
    app.mTop = 275
    app.mLeft = 360

def splash_redrawAll(app):
    # draw title 'sudoku'
    drawBackground(app)
    drawLabel('SUDOKU', 325, 180, size = 60, align = 'center', bold = True, fill = 'black')

    # draw play button
    drawRect(app.bLeft, app.bTop, app.bWidth, app.bHeight, fill = 'lightsteelblue', border = 'black')
    drawRect(app.mLeft, app.mTop, app.mWidth, app.mHeight, fill = 'lightsteelblue', border = 'black')
    drawLabel('PLAY', 215, 305, size = 20, align = 'center')
    drawLabel('MAKE YOUR', 435, 295, size = 14, align = 'center')
    drawLabel('OWN BOARD', 435, 315, size = 14, align = 'center')

def splash_onMousePress(app, mouseX, mouseY):
    if (app.bLeft <= mouseX <= app.bLeft + app.bWidth and
        app.bTop <= mouseY <= app.bTop + app.bHeight):
        setActiveScreen('modes')
    elif (app.mLeft <= mouseX <= app.mLeft + app.mWidth and
        app.mTop <= mouseY <= app.mTop + app.mHeight):
        setActiveScreen('building')

def drawBackground(app):
    drawRect(0, 0, 650, 500, fill = 'floralwhite')

# def main():
#     runAppWithScreens(initialScreen = 'splash', width = 650, height = 500)

# main()