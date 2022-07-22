import sqlite3
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import ttk
from tkinter.messagebox import showinfo


file_path = "B:\Microsoft VS Code\Code.exe"


def ask_time():
    try:
        time = int(input("Enter time in seconds: "))
        return time

    except:
        print("Type only whole numbers!")
        ask_time()


def edit_time(file_path):

    time = ask_time()

    conn = sqlite3.connect('GameTimeTrack\game_time.db')
    c = conn.cursor()
    # update db with new time
    c.execute("""UPDATE game_time SET time = ? WHERE file_path = ?""",
              (time, file_path))
    # commit changes
    conn.commit()
    conn.close()


# edit_time(file_path)


# make edit for name
def ask_name():
    name = str(input("Enter name: "))
    return name


def edit_name(file_path):

    name = ask_name()

    conn = sqlite3.connect('GameTimeTrack\game_time.db')
    c = conn.cursor()
    # update db with new time
    c.execute("""UPDATE game_time SET name = ? WHERE file_path = ?""",
              (name, file_path))
    # commit changes

    conn.commit()
    conn.close()


# edit_name(file_path)


# make edit for file_path


file_path_new = ""


def ask_file_path():
    root = tk.Tk()
    root.title('Choose A Game To Track')
    root.resizable(False, False)
    root.geometry('300x150')
    # make bg color of the window dark grey
    root.configure(background='#2f2f2f')

    def select_file():
        global file_path_new

        filetypes = (
            ('exe files', '*.exe'),
            ('All files', '*.*')
        )

        filename = fd.askopenfilename(
            title='Open a file',
            initialdir='/',
            filetypes=filetypes)

        file_path_new = filename
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
    return file_path_new


def edit_file_path(file_path):

    file_path_new = ask_file_path()

    # check if file_path_new is empty or not
    if file_path_new != "":
        conn = sqlite3.connect('GameTimeTrack\game_time.db')
        c = conn.cursor()
        # update db with new time
        c.execute("""UPDATE game_time SET file_path = ? WHERE file_path = ?""",
                  (file_path_new, file_path))
        # commit changes
        conn.commit()
        conn.close()
        # change file path in games_to_track.db
        conn = sqlite3.connect('GameTimeTrack\games_to_track.db')
        c = conn.cursor()
        # update db with new time
        c.execute("""UPDATE game_time SET file_path = ? WHERE file_path = ?""",
                  (file_path_new, file_path))
        # commit changes
        conn.commit()
        conn.close()

        print("File paths updated!")

    else:
        print("File path is empty!")
        edit_file_path(file_path)


edit_file_path(file_path)
