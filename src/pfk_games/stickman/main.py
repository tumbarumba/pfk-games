import tkinter as tk
from platform import platform

from pfk_games.stickman.images import image_path
from pfk_games.stickman.sprite import PlatformSprite
from pfk_games.stickman.stickman import StickMan


def main() -> None:
    game = StickMan()
    game.mainloop()


if __name__ == "__main__":
    main()
