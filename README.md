# Dice Game

A small Python dice game: roll two six-sided dice; a total of seven wins, and
any other total loses. Play in a terminal or in a browser.

## Web interface

From the directory containing the `dice_game` package, run:

```bash
python3 -m dice_game.web
```

Then open [http://127.0.0.1:8000](http://127.0.0.1:8000). Stop the server
with Ctrl+C. The web server uses only the Python standard library.

## Terminal interface

From the directory containing the `dice_game` package, run:

```bash
python3 -m dice_game
```

Press Enter to roll; enter `q` to quit.

Requires Python 3.10 or later. No third-party packages are needed.

## Tests

From the directory containing the `dice_game` package:

```bash
python3 -m unittest discover -s dice_game/tests
```

## Design

See [DESIGN.md](DESIGN.md) for the domain model and system sequence diagram.
The game runs in memory and has no database.
