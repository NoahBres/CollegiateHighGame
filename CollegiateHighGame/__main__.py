import os
from .game import Game

if __name__ == "__main__":
    os.environ["SDL_VIDEO_CENTERED"] = "1"

    game = Game()
    game.run()
