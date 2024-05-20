import os

print("PixelPlanet.fun timelapse maker")
print("by: PixelHungary")
print("Please DM: 'averagebatyoenjoyer' in discord if you find an issue")
print("")

if os.path.isfile("speed"):
    os.remove("speed")
else:
    pass

a = input("start x,y coordinates: ")
b = input("end x,y coordinates: ")
start_date = input("start time: ")
end_date = input("end time: ")
speed = input("Timelapse speed(fps): ")

f = open("speed", "+a")
f.write(speed)
f.close()

print("image download starting")

cmd_command = "historyDownload.exe 0 ", a, b, start_date, end_date 

cmd_string = " ".join(cmd_command)

os.system(cmd_string)


