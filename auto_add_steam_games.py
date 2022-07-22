from numpy import append
from regex import D
import win32gui
import os
import win32process
import psutil
import time
import sqlite3
import winreg
from pathlib import Path
import vdf
from steampak import SteamApi
import steamfront

# using winreg, find the path of Steam


def get_steam_path():
    try:
        with winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Valve\Steam",
            0,
            winreg.KEY_READ,
        ) as key:
            install_location = Path(
                winreg.QueryValueEx(key, "SteamPath")[0]
            ).absolute()
            return install_location
    except OSError:
        raise Exception("Steam install not found.")


path = str(get_steam_path()) + "\\steamapps\\libraryfolders.vdf"

d = vdf.load(open(path))
d = d["libraryfolders"]
d = dict(d)

# get all keys in d

print(d["0"]["apps"])
print(d["1"]["apps"])

count = 0
for i in d["0"]["apps"]:
    count += 1
for i in d["1"]["apps"]:
    count += 1
print("count: " + str(count))

client = steamfront.Client()


def get_apps_info():
    keys = list(d.keys())
    installed_apps = []
    # Get installed or not. 1 is installed and 0 is not installed
    for val in keys:
        for i in d[f"{val}"]["apps"]:
            appid = i
            game_info_path = f"Software\\Valve\\Steam\\Apps\{appid}"
            try:
                with winreg.OpenKey(
                    winreg.HKEY_CURRENT_USER,
                    game_info_path,
                    0,
                    winreg.KEY_READ,
                ) as key:
                    installed = winreg.QueryValueEx(key, "Installed")[0]

                    try:
                        really_installed = True
                        name = winreg.QueryValueEx(key, "Name")[0]
                        print(f"+{name} install state: {installed} - {appid}")
                    except:
                        really_installed = False
                        try:
                            game = client.getApp(appid=i)
                            print(
                                f"-{game.name} install state: {installed} - {appid}")
                        except:
                            really_installed = False
                            print(f"={appid} install state: {installed}")
                    if installed == 1 and really_installed == True:
                        installed_apps.append(appid)
            except OSError:
                raise Exception("Game install not found.")
    print(installed_apps)


get_apps_info()

client = steamfront.Client()
"""for i in d["0"]["apps"]:
    try:
        game = client.getApp(appid=i)
        print(game.name)
    except:
        pass"""

print("----------------------------------------------------")

"""for i in d["1"]["apps"]:
    game = client.getApp(appid=i)
    print(game.name)"""
"""

applist = [105600, 202970, 212910, 228980, 230410,
           236110, 632360, 892970, 896660, 960090]


for i in applist:
    try:
        game = client.getApp(appid=i)
        print(game.name)
    except:
        pass


path = str(get_steam_path()) + "\\config\\config.vdf"

con = vdf.load(open(path))
print()
poss = con["InstallConfigStore"]["Software"]["valve"]["Steam"]["Tools"]

for i in poss:
    if i != "":
        print(i)"""


"""path = str(get_steam_path()) + "\\steamapps\\libraryfolders.vdf"

d = vdf.load(open(path))
d = d["libraryfolders"]
d = dict(d)

keys = list(d.keys())
different_paths = []
for i in keys:
    different_paths.append(d[i]['path'])

app_dict = {}
for i in different_paths:
    drive_path = i + "\\steamapps\\"
    # get all files that start with appmanifest and end with .acf
    files = os.listdir(drive_path)
    files = [f for f in files if f.startswith(
        "appmanifest") and f.endswith(".acf")]
    for i in files:
        # open the file and convert it to a dictionary
        file_path = drive_path + i
        d = vdf.load(open(file_path))
        d = dict(d)
        # add the values to the app_dict
        if d['AppState']["name"] != "Steamworks Common Redistributables":
            app_dict[d['AppState']['name']] = d['AppState']["appid"]
            # add d['AppState']["installdir"] to the app_dict
            app_dict[d['AppState']['name']] = d['AppState']["installdir"]

print(app_dict)"""
