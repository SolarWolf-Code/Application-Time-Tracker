import sqlite3


file_path = "B:\Microsoft VS Code\Code.exe"


# connect to game_time.db
conn = sqlite3.connect('GameTimeTrack\games_to_track.db')
c = conn.cursor()


# remove the row with the file_name from the db
c.execute("""DELETE FROM game_time WHERE file_path = ?""", (file_path,))
conn.commit()
# close the db
conn.close()

# remove records from a different database as well
conn = sqlite3.connect('GameTimeTrack\game_time.db')
c = conn.cursor()
c.execute("""DELETE FROM game_time WHERE file_path = ?""", (file_path,))
conn.commit()
conn.close()
