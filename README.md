# PFK Games

These contains the (modified) code for [Jason Brigg's](https://jasonrbriggs.com/) book
[Python for Kids](https://jasonrbriggs.com/python-for-kids-2/).

![Python for Kids book cover](https://github.com/jasonrbriggs/python-for-kids/blob/main/cover.jpg)

Original code from the book can be found at [https://github.com/jasonrbriggs/python-for-kids](https://github.com/jasonrbriggs/python-for-kids).
This repository has some changes, and the code has been arranged into a module structure.

To install, clone the repo, cd to the top level directory, and run:

```
pip install -e '.[dev,test]'
```

This repo has the code for `bounce` and `stickman`. You can run those directly as commands from the terminal.
Altenatively, you can specify the full module name:

```
python src/pfk_games/bounce/main.py
```

```
python src/pfk_games/stickman/main.py
```
