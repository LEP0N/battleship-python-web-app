import psycopg2


class PSQL_DB_Worker:
    def __init__(self, host, user, password, database, port=5432):
        self.connection = psycopg2.connect(
            host=host, user=user, password=password, database=database, port=port
        )
        self.cursor = self.connection.cursor()
        self.connection.autocommit = True

    def create_table(self):
        with self.connection:
            self.cursor.execute(
                """CREATE TABLE IF NOT EXISTS ships(
                    id varchar,
                    Aircraft int[][],
                    Battleship int[][],
                    Cruiser int[][],
                    Submarine int[][],
                    Carrier int[][]);"""
            )

    def set_id(self, id):
        with self.connection:
            self.cursor.execute(f"""INSERT INTO ships VALUES ('{id}');""")

    def update_coords(self, id, ship_name, positions):
        with self.connection:
            self.cursor.execute(
                f"""UPDATE ships SET {ship_name}=ARRAY{positions} WHERE id='{id}';"""
            )
