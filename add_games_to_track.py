# create a new sql database

from tkinter.messagebox import showinfo
from tkinter import filedialog as fd
from tkinter import ttk
import sqlite3
import pandas
import tkinter as tk

# create a new database
conn = sqlite3.connect('GameTimeTrack\games_to_track.db')


# create a cursor
c = conn.cursor()


# make a tkinter window to pick an exe file


# create the root window
root = tk.Tk()
root.title('Choose A Game To Track')
root.resizable(False, False)
root.geometry('300x150')
# make bg color of the window dark grey
root.configure(background='#2f2f2f')
GAME_LIST = []


def select_file():
    global GAME_LIST

    filetypes = (
        ('exe files', '*.exe'),
        ('All files', '*.*')
    )

    filename = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes)

    GAME_LIST.append(filename)
    # close the window
    root.destroy()


# open button
open_button = ttk.Button(
    root,
    text='Open a File',
    command=select_file,
)

open_button.pack(expand=True)


# run the application
root.mainloop()


if GAME_LIST != []:
    for game in GAME_LIST:
        if game != '':

            c.execute("""INSERT INTO game_time (file_path) VALUES (?)""", (game,))

            # commit the changes
            conn.commit()
            # close the connection
            conn.close()

            print(f"Now tracking: {game}")
