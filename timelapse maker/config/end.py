import os
import shutil
print(" Timelapse sucessfully created, you can close this window now")
print(" You can find the timelapse in the config folder !")
shutil.rmtree('images')
shutil.rmtree('timelapse')
os.mkdir("images")
os.mkdir("timelapse")
input()
