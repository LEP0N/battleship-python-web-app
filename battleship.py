from random import choice, randint
from PSQL_DB import PSQL_DB_Worker
import uuid


host = "127.0.0.1"
user = "lep0n"
password = ""
db = "battleship"
port = 5432

worker = PSQL_DB_Worker(host, user, password, db, port)


class Ship:
    def __init__(self, name: str, x: int, y: int, size: int, direction: str):
        self.name = name
        self.x = x
        self.y = y
        self.size = size
        self.direction = direction
        self.hp = size
        self.set_w_h(direction)

    def __str__(self):
        return Cell.empty_cell

    def set_w_h(self, direction: str):
        """Calculating the width and height of the ship."""

        self.direction = direction

        if self.direction == "right":
            self.width = self.size
            self.height = 1
        elif self.direction == "up":
            self.width = 1
            self.height = self.size
        elif self.direction == "left":
            self.width = self.size
            self.height = 1
        elif self.direction == "down":
            self.width = 1
            self.height = self.size


class Cell:
    """Types of field cell."""

    empty_cell = " "
    miss_cell = "•"
    damaged_cell = "X"


class Grid:
    def __init__(self, size=10):
        self.grid = [[Cell.empty_cell] * size for _ in range(size)]
        self.size = size
        self.id = uuid.uuid4().hex
        self.ships = {
            "Aircraft": 5,
            "Battleship": 4,
            "Cruiser": 3,
            "Submarine": 3,
            "Carrier": 2,
        }
        self.alive_ships = list()
        worker.create_table()
        worker.set_id(self.id)

    def initialise_grid(self):
        """Returns the grid for the field."""

        return self.grid

    def add_ship(self, ship):
        """Adds a ship to the field."""

        x, y = ship.x, ship.y
        width, height = ship.width, ship.height
        ship_position = list()

        for field_x in range(x, x + height):
            for field_y in range(y, y + width):
                self.grid[field_x][field_y] = ship
                ship_position.append([field_x, field_y])

        worker.update_coords(self.id, ship.name, ship_position)
        self.ships[ship.name] = ship_position
        self.alive_ships.append(ship)

    def check_ship_collision(self, ship) -> bool:
        """Checks whether the ship can be placed on the field."""

        x, y = ship.x, ship.y
        width, height = ship.width, ship.height

        if x + height - 1 >= self.size or x < 0 or y + width - 1 >= self.size or y < 0:
            return False

        for field_x in range(x - 1, x + height + 1):
            for field_y in range(y - 1, y + width + 1):
                if (
                    field_x < 0
                    or field_x >= self.size
                    or field_y < 0
                    or field_y >= self.size
                ):
                    continue
                if type(self.grid[field_x][field_y]) == Ship:
                    return False

        return True

    def generate_ships(self):
        """Generates ships on the field."""

        directions = ["right", "up", "left", "down"]

        for s in self.ships:
            while True:
                ship = Ship(
                    s, randint(0, 10), randint(0, 10), self.ships[s], choice(directions)
                )

                if self.check_ship_collision(ship):
                    self.add_ship(ship)
                    break

    def destroy_ship(self, ship):
        """Surrounds the destroyed ship with misses."""

        x, y = ship.x, ship.y
        width, height = ship.width, ship.height

        for field_x in range(x - 1, x + height + 1):
            for field_y in range(y - 1, y + width + 1):
                if (
                    field_x < 0
                    or field_x >= self.size
                    or field_y < 0
                    or field_y >= self.size
                ):
                    continue

                self.grid[field_x][field_y] = Cell.miss_cell

        for field_x in range(x, x + height):
            for field_y in range(y, y + width):
                self.grid[field_x][field_y] = Cell.damaged_cell

    def fire(self, x: int, y: int) -> str:
        """Makes a shot at the coordinates of the field."""

        if 0 <= x <= 9 and 0 <= y <= 9:
            if self.grid[x][y] == Cell.empty_cell:
                self.grid[x][y] = Cell.miss_cell
                return "miss"

            elif type(self.grid[x][y]) == Ship:
                ship = self.grid[x][y]
                ship.hp -= 1

                for s in self.ships:
                    if [x, y] in self.ships[s]:
                        self.ships[s].remove([x, y])

                if ship.hp == 0:
                    self.destroy_ship(ship)
                    self.alive_ships.remove(ship)
                    return "kill"

                self.grid[x][y] = Cell.damaged_cell
                return "injure"
