import os

print("PixelPlanet.fun timelapse maker")
print("by: Batyo")
print("")

a = input("start x,y coordinates: ")
b = input("end x,y coordinates: ")
start_date = input("start time: ")
end_date = input("end time: ")

print("image download starting")

cmd_command = [
    r"historyDownload.exe",
    "0",
    a,
    b,
    start_date,
    end_date
]

cmd_string = " ".join(cmd_command)

os.system(cmd_string)

