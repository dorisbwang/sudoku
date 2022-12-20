# general outline of main taken from Kozbie's screen demos

from cmu_cs3_graphics import *
from screenfunctions import *
from stateclass import State
from player import *
from splash import *
from modes import *
from building import *
from help import *


##################################
# main
##################################

def main():
    runAppWithScreens(initialScreen = 'splash', width = 650, height = 500)

main()
