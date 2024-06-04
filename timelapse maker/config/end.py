import os
import shutil
print(" Timelapse sucessfully created, you can close this window now")

if os.path.isfile("outputpath.txt"):
    f = open("outputpath.txt", "r")
    a = f.read()
    print(" You can find the timelapse in ", a ," !")
else:
    print(" You can find the timelapse in the desktop !")
print(" If you cant find the timelapse video, then use windows searcher, and search for it.")
shutil.rmtree('images')
os.mkdir("images")
input()
