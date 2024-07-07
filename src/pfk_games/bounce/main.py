from pfk_games.bounce.bounce import Bounce


def main() -> None:
    game = Bounce()
    game.mainloop()
    print("Game Over")


if __name__ == "__main__":
    main()
