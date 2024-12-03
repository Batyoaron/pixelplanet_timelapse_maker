import os

if os.path.isfile("config/input.exe"):
    pass
else:
    print(" [!] Didnt found any file to open \n\n Possible errors: \n [1]: Antivirus blocked to open the application \n [2]: You only extracted this file, which is not enough")
    input(" \n enter to quit")
    exit()

os.chdir("Config")
os.system("input.exe")
