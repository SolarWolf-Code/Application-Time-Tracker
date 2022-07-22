import win32gui
import os
import win32process
import psutil
import time
import sqlite3


# get a list of all the current active windows and their names

TIME_RAN = 0
start_time = 0


def games_to_track():
    GAME_LIST = []
    conn = sqlite3.connect('GameTimeTrack\games_to_track.db')
    # print all rows in db
    c = conn.cursor()
    c.execute("""SELECT * FROM game_time""")
    for row in c.fetchall():
        GAME_LIST.append(row[0])
    conn.close()
    return GAME_LIST


def add_to_db(name, time, last_access_time, file_path):
    conn = sqlite3.connect('GameTimeTrack\game_time.db')
    c = conn.cursor()
    # if game already in db, update time and last_access_time
    # if not, add game to db with all values
    c.execute("""SELECT * FROM game_time""")

    for row in c.fetchall():
        if row[0] == name:
            c.execute("""UPDATE game_time SET time = ?, last_access_time = ? WHERE name = ?""",
                      (time, last_access_time, name))
            conn.commit()
            break
    else:
        c.execute("""INSERT INTO game_time (name, time, last_access_time, file_path) VALUES (?, ?, ?, ?)""",
                  (name, time, last_access_time, file_path))
        conn.commit()
    conn.close()


def get_active_windows():
    windows = []
    win32gui.EnumWindows(lambda hwnd, windows: windows.append(
        (hwnd, win32gui.GetWindowText(hwnd))), windows)
    get_window_path(set(windows))


proc_start_times = {}
proc_prev_time = {}


def get_window_path(list_of_windows):
    global start_time
    global TIME_RAN

    windows_to_add = []

    for window in list_of_windows:
        # if window[1] is not equal to any of the index [1] of windows_to_add, add it to windows_to_add
        if window[1] not in [windows_to_add[i][1] for i in range(len(windows_to_add))]:
            windows_to_add.append(window)

    # get the process ID of the window
    window_paths = []
    for window in windows_to_add:
        pid = win32process.GetWindowThreadProcessId(window[0])[1]
        # check if pid is positive int
        if pid > 0:
            proc_process = psutil.Process(pid)
            # proc_name = proc_process.name().replace(".exe", "")
            proc_path = proc_process.exe()
            # print(proc_path)
            window_paths.append(proc_path)

    window_paths = list(set(window_paths))

    # if game from GAME_LIST is in window_paths
    for window in window_paths:
        if window in games_to_track():

            # check if window is already in proc_start_times and is not in window_paths

            for win in proc_start_times:
                if win not in window_paths:
                    proc_start_times.pop(win)

            if window not in proc_start_times:
                start_time = time.time()
                proc_start_times[window] = start_time

            else:
                # print(window)
                start_time = proc_start_times[window]

            name = window.split("\\")[-1]

            # check if window is in game_time.db
            conn = sqlite3.connect('GameTimeTrack\game_time.db')
            c = conn.cursor()
            c.execute("""SELECT * FROM game_time""")
            for row in c.fetchall():
                if window == row[3]:
                    name = row[0]

            end_time = time.time()

            # open db and read time value for window name.

            conn = sqlite3.connect('GameTimeTrack\game_time.db')
            c = conn.cursor()

            # check db if name is present and equal to window name.
            c.execute("""SELECT * FROM game_time""")

            add_time = round(end_time - start_time)

            if window not in proc_prev_time:
                proc_prev_time[window] = 0

            else:
                prev_time = proc_prev_time[window]
                proc_prev_time[window] = add_time

            for row in c.fetchall():
                if row[0] == name:
                    if proc_prev_time[window] != 0:
                        time_in_db = round(row[1])
                        TIME_RAN = add_time + time_in_db - prev_time
                        break
                    else:
                        time_in_db = round(row[1])
                        TIME_RAN = add_time + time_in_db
                        break

            else:
                TIME_RAN = end_time - start_time

            #TIME_RAN = end_time - start_time

            print(f"{window} has been running for {TIME_RAN} seconds total")
            # add data to db
            last_access_time = os.path.getatime(window)
            if last_access_time < end_time:
                last_access_time = end_time

            last_access_time = time.strftime(
                "%Y-%m-%d %H:%M:%S", time.localtime(last_access_time))

            add_to_db(name, TIME_RAN, last_access_time, window)
        else:
            # Update all game last played times regardless of whether the game is open or not
            conn = sqlite3.connect('GameTimeTrack\game_time.db')
            c = conn.cursor()
            c.execute("""SELECT * FROM game_time""")
            for row in c.fetchall():
                file_path = row[3]
                name = row[0]
                last_access_time = os.path.getatime(file_path)
                last_access_time = time.strftime(
                    "%Y-%m-%d %H:%M:%S", time.localtime(last_access_time))
                c.execute("""UPDATE game_time SET last_access_time = ? WHERE name = ?""",
                          (last_access_time, name))
                conn.commit()


while True:
    time.sleep(1)
    get_active_windows()
    # print(proc_start_times)
    print("---------------------")
