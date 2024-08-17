import tkinter as tk
from pfk_games.stickman.images import image_path
from pfk_games.stickman.sprite import PlatformSprite
from pfk_games.stickman.stickman import StickMan


def main() -> None:
    game = StickMan()
    platform1 = PlatformSprite(game, tk.PhotoImage(image_path("platform1.png")), 0, 480, 100, 10)
    game.sprites.append(platform1)
    game.mainloop()


if __name__ == "__main__":
    main()
