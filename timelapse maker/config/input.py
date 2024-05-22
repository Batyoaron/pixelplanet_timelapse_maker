import os

print("PixelPlanet.fun timelapse maker")
print("by: PixelHungary")
print("Please DM: 'averagebatyoenjoyer' in discord if you find an issue")
print("")

if os.path.isfile("speed"):
    os.remove("speed")
else:
    pass

if os.path.isfile("date"):
    os.remove("date")
else:
    pass



a = input("start x,y coordinates: ")
b = input("end x,y coordinates: ")
startdate = input("start time: ")
enddate = input("end time: ")
speed = input("Timelapse speed(fps): ")

date = (" [D] Start date: " + startdate + "    |  End date: " + enddate)

f = open("speed", "+a")
f.write(speed)
f.close()

f = open("date", "+a")
f.write(str(date))
f.close()

print("image download starting")
cmd_command = "historyDownload.exe 0 ", a, b, startdate, enddate 
cmd_string = " ".join(cmd_command)
os.system(cmd_string)


