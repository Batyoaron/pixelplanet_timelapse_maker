import subprocess
import os

print("PixelPlanet.fun timelapse maker")
print("by: Batyo")
print("")

a = input("start x,y coordinates: ")
b = input("end x,y coordinates: ")
c = input("start time: ")
d = input("end time: ")

print("image download starting")
script_dir = os.path.dirname(os.path.realpath(__file__))
history_download_script = os.path.join(script_dir, "historyDownload.py")

cmd_command = [
    "python",  
    history_download_script,
    "0",
    a,
    b,
    c,
    d
]

result = subprocess.run(cmd_command, capture_output=True, text=True)
if result.returncode == 0:
    print("Output:")
    print(result.stdout)
else:
    print("Error:")
    print(result.stderr)

