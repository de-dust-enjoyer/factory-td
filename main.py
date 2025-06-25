from game import Game
from time import time

pastTime = time()

if __name__ == "__main__":
    game = Game()
    presentTime = time()
    print(f"entered main loop with loading time of {round(presentTime-pastTime, 2)} seconds.")
    game.run()