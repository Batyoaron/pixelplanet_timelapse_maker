import subprocess


print("PixelPlanet.fun timelapse maker")
print("by: Batyo")
print("")

a = input("start x,y coordinates: ")
b = input("end x,y coordinates: ")
c = input("start time: ")
d = input("end time: ")

print("image download starting")
# its historyDownload.exe in the exe version
cmd_command = [
    r"historyDownload.py",
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
