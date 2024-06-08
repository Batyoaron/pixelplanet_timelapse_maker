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
if os.path.isfile("date"):
    os.remove("date")
if os.path.isfile("days"):
    os.remove("days")
if os.path.isfile("name"):
    os.remove("name")

settingsmenu = '''
 [S] Settings Menu
 
 [1]: Set where to save the timelapse 
 [q]: Quit

'''

presetmenu = '''
 [P] Preset Menu

 [1]: Make preset
 [2]: Load preset
 [3]: Delete preset
 [q]: Quit

'''

#menu
menu = '''
 [M] Menu

 [1]: Make timelapse now
 [2]: Presets
 [3]: Settings

'''

#main menu
print(menu)
menuuu = input(" [Choose an option]: ")

if menuuu == "3":
    os.system("cls")
    print(settingsmenu)
    stsmenu = input(" [Choose an option]: ")

    if stsmenu == "q":
        os.startfile("input.exe")
        exit()

    if stsmenu == "1":
        if os.path.isfile("outputpath.txt"):
            os.remove("outputpath.txt")
        f = open("outputpath.txt", "a+")

        savetimelapse = input("\n [Drag the folder into this window]: ")
        f.write(savetimelapse)
        print(" Changes saved !")
        print(" Quitting in 3 seconds...")
        f.close()
        time.sleep(3)
        os.startfile("input.exe")
        exit()


#presets menu
if menuuu == "2":
    os.system("cls")
    print(presetmenu)
    menuu = input(" [Choose an option]: ")

    if menuu == "q":
        os.startfile("input.exe")
        exit()

#create preset

    if menuu == "1":
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


#load preset

    if menuu == "2":
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
        nametimelapsep = choosepreset
        print("")
        print(" Start cordinates for current preset: " , loadpresetcordss)
        print(" End cordinates for current preset: " ,loadpresetcordse)
        startdateload = input(" [Start date]: ")
        enddateload = input(" [End date]: ")
        speedload = input(" [Speed(fps)]: ")


        def count_days(start_date, end_date):
            start_datetime = datetime.strptime(start_date, "%Y-%m-%d")
            end_datetime = datetime.strptime(end_date, "%Y-%m-%d")
            delta = end_datetime - start_datetime
            num_days = delta.days + 1 
            return num_days
        days = count_days(startdateload, enddateload)
        dayss = days

        #name write
        f = open("name", "a")
        f.write(str(nametimelapsep))
        f.close()

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
        time.sleep(2)
        exit()

    

# delete presets

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
if menuuu == "1":
    os.system("cls")
    print("\n [T] Timelapse maker\n")
    nametimelapse = input(" Name of the video: ")
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

    #name write
    f = open("name", "a")
    f.write(str(nametimelapse))
    f.close()

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

    print(" image download starting")
    cmd_command = "historyDownload.exe 0 ", a, b, startdate, enddate  ### REPLACE WITH  EXE WHEN CONVERTED
    cmd_string = " ".join(cmd_command)
    os.system(cmd_string)
    time.sleep(2)
    exit()


print("\n Only use the options that are available")
time.sleep(3)
os.startfile("input.exe")
exit()

