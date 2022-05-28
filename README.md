# ⛵️ Battleship python web app on Flask
## ⚙ Configuration
For the database to work, you need to run the PostgresSQL server and create a file db_config.py, which will store your Postgres settings:  
```python
host = ""  
user = ""  
password = ""  
db = "battleship"  
port = 5432
```
## 📄 Task
Design and implement a (partial) Battleship game as a web app.

In Battleship, the computer has positioned five ships of various sizes on a 10x10 board. Each ship must be placed horizontally or vertically, completely on the board, without overlapping another ship. The player cannot see the ship locations. Each round, the player “fires” at a board position of his choosing. The computer indicates if this was a “hit” or a “miss”. When all tiles of a particular ship have been hit, the computer indicates that the entire ship has been sunk. When the player has sunk all of the ships, the game is over.

Obviously this game would be more fun if the player had his own ships and the computer were firing back, but we’ll leave that out for simplicity. In other words, we are only implementing the turns for Player 1, not for Player 2.

As for the server side you should supply CRUD (create read update delete), for Ship Layouts and game itself.

As for game you do not need to implement any Ai for games and specify ability to select multiplayer
You just may account that you need to win game in shortest count of moves. So you may store number of moves on server side.
## 🖼 Preview
![Preview](https://i.imgur.com/TQzEMzG.png)