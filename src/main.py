import pygame
import sys

from GUI import GUI


def main():
    pygame.init()

    gui_instance = GUI()
    gui_instance.run()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

