import os
print(" Timelapse sucessfully created, you can close this window now")

try:
    with open("convertercommand", 'r') as file:
        remover = file.read()
except FileNotFoundError:
    print(f"File not found.")

os.remove(remover)

if os.path.isfile("outputpath.txt"):
    f = open("outputpath.txt", "r")
    a = f.read()
    print(" You can find the timelapse in ", a ," !")
else:
    print(" You can find the timelapse in the desktop !")
print(" If you cant find the timelapse video, then use windows searcher, and search for it.")
print(" If you can see two videos, delete the one that has NO underscore in the end of its name")
os.remove("convertercommand")
os.remove("convertercommandsecond")
input()
