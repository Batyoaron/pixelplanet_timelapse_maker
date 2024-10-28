import os
import requests
import zipfile
import ctypes
import shutil
import winshell


# checking if porgram running as admin
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if __name__ == "__main__":
    if is_admin():
        pass
    else:
        os.system("cls")
        print("\n Please run the program as administrator, i promise its not harmful c:")
        input()









if os.path.isfile("C:/pixelplanet_timelapse_maker"):
    print(" Pixelplanet timelapse maker is existing, checking for updates...")

os.mkdir("C:/pixelplanet_timelapse_maker")
os.mkdir("C:/pixelplanet_timelapse_maker/application")


def download_and_decompress(url, download_path, extract_path):
    if not isinstance(download_path, str):
        raise TypeError(f"Expected 'download_path' to be a str, got {str(download_path)}")
    if not isinstance(extract_path, str):
        raise TypeError(f"Expected 'extract_path' to be a str, got {str(extract_path)}")

    print("Starting download...")
    response = requests.get(url)
    
    with open(download_path, 'wb') as file:
        file.write(response.content)
    print(f"Downloaded to {download_path}")
    
    os.makedirs(extract_path, exist_ok=True)
    
    print("Starting decompression...")
    with zipfile.ZipFile(download_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)
    print(f"Decompressed to {extract_path}")
    
    os.remove(download_path)
    print(f"Removed the zip file {download_path}")

url = f"https://github.com/Batyoaron/pixelplanet_timelapse_maker/releases/download/ptm1.4.7/pixelplanet_timelapse_maker.zip"

download_path = os.path.join("C:/pixelplanet_timelapse_maker/application/", "pixelplanet_timelapse_maker.zip")
extract_path = os.path.join("C:/pixelplanet_timelapse_maker/application/") 

download_and_decompress(url, download_path, extract_path)


desktop_path = os.path.join(os.environ["USERPROFILE"], "Desktop")

if os.path.isdir("C:/Users/user/Desktop"):
    if " " in desktop_path:
        print(" Error in getting desktop path | Path contains 'Space' in the path")
        pass
    
    else:
        os.chdir("C:/Users/user/Desktop")
        desktop_path = os.getcwd()
        print(" \nDesktop path found")
        f = open("C:/pixelplanet_timelapse_maker/application/pixelplanet_timelapse_maker/config/outputpath.txt", "a")
        f.write(desktop_path)
        f.close()

elif os.path.isdir(desktop_path):
    if " " in desktop_path:
        print(" Error in getting desktop path | Path contains 'Space' in the path")
        pass
    
    else:
        os.chdir(desktop_path)
        print(" Desktop path found")
        f = open("C:/pixelplanet_timelapse_maker/application/pixelplanet_timelapse_maker/config/outputpath.txt", "a")
        f.write(desktop_path)
        f.close()

else:
    print("Desktop not found, you must set up the path manually in the app")


try:
    with open("C:/pixelplanet_timelapse_maker/application/pixelplanet_timelapse_maker/config/outputpath.txt", 'r') as file:
        shortcut_path_desktop = file.read().strip()
except FileNotFoundError:
    print("outputpath not found")
    exit()


current_directory = os.path.dirname(os.path.abspath(__file__))
shortcut_path = os.path.join(current_directory, "pixelplanet_timelapse_maker.lnk")

target_path = "C:/pixelplanet_timelapse_maker/application/pixelplanet_timelapse_maker/launcher.exe"

with winshell.shortcut(shortcut_path) as shortcut:
    shortcut.path = target_path
    shortcut.description = "shortcut for ptm"  
    shortcut.icon_location = (target_path, 0)

fromm = os.path.join(current_directory, "pixelplanet_timelapse_maker.lnk")  
to = shortcut_path_desktop

if os.path.isfile("C:/Users/user/Desktop/pixelplanet_timelapse_maker.lnk"):
    pass
else:
    shutil.move(fromm, to)