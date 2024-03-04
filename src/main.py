import pygame
import sys

from game import Game
from GUI import GUI


def main():
    pygame.init()
    
    game_instance = Game(9)
    gui_instance = GUI(game_instance)
    gui_instance.run()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

