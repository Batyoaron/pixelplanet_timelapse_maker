import os
import shutil
print(" Timelapse sucessfully created, you can close this window now")
print(" You can find the timelapse in the desktop !")
shutil.rmtree('images')
shutil.rmtree('timelapse')
os.mkdir("images")
os.mkdir("timelapse")
