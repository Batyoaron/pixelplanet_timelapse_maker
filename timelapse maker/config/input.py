import os
from datetime import datetime
import time
import shutil

os.system("cls")

maintext = '''
 PixelPlanet.fun timelapse maker
 By: PixelHungary
 Please DM: 'averagebatyoenjoyer' in discord if you find an issue

'''
print(maintext)

if os.path.isfile("speed"):
    os.remove("speed")
else:
    pass

if os.path.isfile("date"):
    os.remove("date")
else:
    pass

if os.path.isfile("days"):
    os.remove("days")
else:
    pass




#menu
menu = '''
 [M] Menu

 [1]: Make timelapse now
 [2]: Make preset
 [3]: Load preset 
 [4]: Delete preset 

'''
print(menu)

menuu = input(" [Please choose an option]: ")

if menuu == "2":
    os.system("cls")
    print("\n [M] Make preset \n You can make one now, and load one later and you dont need to copy the cordinates again")
    print(" Press 'q' and enter if you want to exit \n")
    npreset = input(" [Name your preset]: ")
    if npreset == "q":
        os.startfile("input.exe") ######REWRITE WHEN CONVERTED TO EXE
        exit()
    cordss = input(" [Start x,y coordinates]:  ")
    cordse = input(" [End x,y coordinates]:  ")
    
    full_path = os.path.join("presets", npreset)
    full_pathh = os.path.join(full_path, "cordss.txt")
    full_pathhh = os.path.join(full_path, "cordse.txt")

    os.mkdir(full_path)

    f = open(full_pathhh, "a+")
    f.write(cordse)
    f.close()

    f = open(full_pathh, "a+")
    f.write(cordss)
    f.close()
    print("\n Preset ", npreset, " Saved sucessfully, restarting in 3 seconds...")
    time.sleep(3)
    os.startfile("input.exe") ### REPLACE WITH  EXE WHEN CONVERTED
    exit()

    

if menuu == "3":
    os.system("cls")
    print("Presets: \n")
    def list_directories(path):
        try:
            contents = os.listdir(path)
            for item in contents:
                if os.path.isdir(os.path.join(path, item)):
                    print(item)
        except FileNotFoundError:
            print("The specified directory does not exist.")
    directory_path = "presets"
    list_directories(directory_path)
    print("\nPress 'q' and enter if you want to exit")
    choosepreset = input("[Type your preset name to chooose it]: ")
    if choosepreset == "q":
        os.startfile("input.exe") ######REWRITE WHEN CONVERTED TO EXE
        exit()

    loadpresetcordss = "" 
    loadpresetcordse = "" 

    try:
        with open("presets/" + choosepreset + "/cordss.txt", 'r') as file:
              loadpresetcordss = file.read()
    except FileNotFoundError:
            print(f"File not found.")
    try:
        with open("presets/" + choosepreset + "/cordse.txt", 'r') as file:
            loadpresetcordse = file.read()
                    
    except FileNotFoundError:
        print(f"File not found.")

    os.system("cls")
    print(" [L] Load presets")
    print(" [C] Current preset: ",choosepreset)
    print("")
    print(" Start cordinates for current preset: " , loadpresetcordss)
    print(" End cordinates for current preset: " ,loadpresetcordse)
    startdateload = input(" [Start date]: ")
    enddateload = input(" [End date]: ")
    speedload = input(" [Speed]: ")


    def count_days(start_date, end_date):
        start_datetime = datetime.strptime(start_date, "%Y-%m-%d")
        end_datetime = datetime.strptime(end_date, "%Y-%m-%d")
        delta = end_datetime - start_datetime
        num_days = delta.days + 1 
        return num_days
    days = count_days(startdateload, enddateload)
    dayss = days


    #days write
    f = open("days", "a")
    f.write(str(dayss))
    f.close()

    #speed write
    f = open("speed", "+a")
    f.write(speedload)
    f.close()

    #date write
    date = (" [D] Start date: " + startdateload + "    |  End date: " + speedload)
    f = open("date", "+a")
    f.write(str(date))
    f.close()


    cmd_command = "historyDownload.exe 0 ", loadpresetcordss, loadpresetcordse, startdateload, enddateload  ### REPLACE WITH  EXE WHEN CONVERTED
    cmd_string = " ".join(cmd_command)
    os.system(cmd_string)
    exit()

    



if menuu == "4":
    os.system("cls")
    print("Presets: \n")
    def list_directories(path):
        try:
            contents = os.listdir(path)
            for item in contents:
                if os.path.isdir(os.path.join(path, item)):
                    print(item)
        except FileNotFoundError:
            print("The specified directory does not exist.")
    directory_path = "presets"
    list_directories(directory_path)
    print("\nPress 'q' and enter if you want to exit")
    choosepresetdelete = input("[Type your preset name to delete it]: ")  

    if choosepresetdelete == "q":
        os.startfile("input.exe") ######REWRITE WHEN CONVERTED TO EXE
        exit()

    shutil.rmtree("presets/" + choosepresetdelete)
    print(choosepresetdelete, " Deleted sucessfully, restarting in 3 seconds")
    time.sleep(3)
    os.startfile("input.exe") ###### REWRITE TO .EXE WHEN CONVERTED
    exit()


#### main timelapse maker
if menuu == "1":
    pass

os.system("cls")
print(maintext)
print(" [T] Timelapse maker\n")
a = input(" Start x,y coordinates: ")
b = input(" End x,y coordinates: ")
startdate = input(" Start time: ")
enddate = input(" End time: ")
speed = input(" Timelapse speed(fps): ")


def count_days(start_date, end_date):
    start_datetime = datetime.strptime(start_date, "%Y-%m-%d")
    end_datetime = datetime.strptime(end_date, "%Y-%m-%d")
    delta = end_datetime - start_datetime
    num_days = delta.days + 1 
    return num_days
days = count_days(startdate, enddate)
dayss = days

#days write
f = open("days", "a")
f.write(str(dayss))
f.close()

#speed write
f = open("speed", "+a")
f.write(speed)
f.close()

#date write
date = (" [D] Start date: " + startdate + "    |  End date: " + enddate)
f = open("date", "+a")
f.write(str(date))
f.close()

print("image download starting")
cmd_command = "historyDownload.exe 0 ", a, b, startdate, enddate  ### REPLACE WITH  EXE WHEN CONVERTED
cmd_string = " ".join(cmd_command)
os.system(cmd_string)


