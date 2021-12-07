from flask import Flask, render_template, url_for, request, redirect
from battleship import *


app = Flask(__name__)
app.secret_key = "some_secret"


field = Grid()
field.generate_ships()

move = 0


@app.route("/")
def index():
    """Main page."""
    print(field.ships)
    return render_template(
        "index.html",
        grid=field.initialise_grid(),
        cell=Cell(),
        alive_ships=len(field.alive_ships),
        ships=field.ships,
        move=move,
    )


@app.route("/fire")
def fire():
    """Makes a shot at the coordinates of the field."""

    global move

    row = request.args.get("rowIndex", default=-1, type=int)
    column = request.args.get("columnIndex", default=-1, type=int)

    result = field.fire(row, column)

    move += 1
    print(move, result)

    return redirect(url_for("index"))


@app.route("/restart")
def restart():
    """Restart game."""

    global field, move
    field = Grid()
    field.generate_ships()

    move = 0

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run()
