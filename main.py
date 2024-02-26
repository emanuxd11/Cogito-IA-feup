from GUI import GUI
from game import Game

def main():
    game_instance = Game(9)
    gui_instance = GUI(game_instance)
    gui_instance.run()

if __name__ == "__main__":
    main()

