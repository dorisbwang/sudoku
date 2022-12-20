from cmu_cs3_graphics import *
from screenfunctions import *
from stateclass import State
import math
import os
import random
from modes import *
import copy

def help_onScreenStart(app):
    app.hint1 = 'SHOW SINGLES (s): highlights cells that contain singletons'
    app.hint2 = 'PLAY SINGLES (S): plays a single cell that contains a singleton'
    app.hint3 = 'PLAY ALL SINGLES (L): plays all cells that conain singletons'
    app.hint4 = 'SHOW HINT 2 (h): show N cells that contain N unique legal values'
    app.hint5 = 'PLAY HINT 2 (H): bans the N unique legal values from all regions' 
    app.hint55 = 'that the N cells share'
    app.hint6 = 'RED DOT: appears when the value entered is not aligned with the'
    app.hint65 = 'solution value of the cell, or if the solution value was banned from the cell'
    app.hint7 = 'SAVE BOARD AS PDF (b): saves the starting and current board'
    app.hint75 = 'as a two-page PDF file, saved as boards.pdf'

def help_redrawAll(app):
    drawBackground(app)

    drawLabel('Help', 50, 35, size=20, align = 'left', bold = True)
    drawLabel(f'{app.hint1}', 50, 75, size = 16, align = 'left')
    drawLabel(f'{app.hint2}', 50, 100, size = 16, align = 'left')
    drawLabel(f'{app.hint3}', 50, 125, size = 16, align = 'left')
    drawLabel(f'{app.hint4}', 50, 150, size = 16, align = 'left')
    drawLabel(f'{app.hint5}', 50, 175, size = 16, align = 'left')
    drawLabel(f'{app.hint55}', 50, 200, size = 16, align = 'left')
    drawLabel(f'{app.hint6}', 50, 250, size = 16, align = 'left')
    drawLabel(f'{app.hint65}', 50, 275, size = 16, align = 'left')
    drawLabel(f'{app.hint7}', 50, 300, size = 16, align = 'left')
    drawLabel(f'{app.hint75}', 50, 325, size = 16, align = 'left')

    drawRect(250, 395, 150, 60, fill = 'lightsteelblue', border = 'black')
    drawLabel('BACK', 325, 425, size = 20, align = 'center')

def help_onMousePress(app, mouseX, mouseY):
    if 250 <= mouseX <= 250 + 150 and 395 <= mouseY <= 395 + 60:
        setActiveScreen('player')

def drawBackground(app):
    drawRect(0, 0, 650, 500, fill = 'floralwhite')
    
# def main():
#     runAppWithScreens(initialScreen = 'help', width = 650, height = 500)

# main()
