import requests
import os
import zipfile
import shutil
import winshell

try:
    with open("config/new_version.txt", 'r') as file:
        new_version = file.read().strip()
        new_version = "ptm" + new_version
except FileNotFoundError:
    exit()


try:
    with open("config/outputpath.txt", 'r') as file:
        shortcut_path_desktop = file.read().strip()
except FileNotFoundError:
    exit()

## saving old data

shutil.copytree("config/presets", "C:/pixelplanet_timelapse_maker/application/pixelplanet_timelapse_maker/presets_save", dirs_exist_ok=True)
if os.path.isfile("config/outputpath.txt"):
    shutil.move("C:/pixelplanet_timelapse_maker/application/pixelplanet_timelapse_maker/config/outputpath.txt", "C:/pixelplanet_timelapse_maker/application/pixelplanet_timelapse_maker")


shutil.rmtree("config")
get_path_for_new_version = "config/"

def download_and_decompress(url, download_path, extract_path):
    if not isinstance(download_path, str):
        raise TypeError(f"Expected 'download_path' to be a str, got {str(download_path)}")
    if not isinstance(extract_path, str):
        raise TypeError(f"Expected 'extract_path' to be a str, got {str(extract_path)}")


def download_and_decompress(url, download_path, extract_path):
    print("Starting download...")
    response = requests.get(url)
    
    with open(download_path, 'wb') as file:
        file.write(response.content)
    print(f"Downloaded to {download_path}")
    
    print("Starting decompression...")
    with zipfile.ZipFile(download_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)
    print(f"Decompressed to {extract_path}")
    
    os.remove(download_path)
    print(f"Removed the zip file {download_path}")

url = f"https://github.com/Batyoaron/pixelplanet_timelapse_maker/releases/download/{new_version}/pixelplanet_timelapse_maker_debug.zip"



current_path = os.getcwd()
download_path = os.path.join(current_path, "pixelplanet_timelapse_maker.zip")  
extract_path = current_path 

download_and_decompress(url, download_path, extract_path)

source_dir = "presets_save/"
dest_dir = "config/presets/"
os.makedirs(dest_dir, exist_ok=True)

for item in os.listdir(source_dir):
    src_path = os.path.join(source_dir, item)
    dest_path = os.path.join(dest_dir, item)

    if os.path.isdir(src_path):
        shutil.copytree(src_path, dest_path, dirs_exist_ok=True)
    else:
        shutil.copy2(src_path, dest_path)

shutil.move("outputpath.txt", "config/")

current_directory = os.path.dirname(os.path.abspath(__file__))
shortcut_path = os.path.join(current_directory, "pixelplanet_timelapse_maker.lnk")

target_path = "C:/pixelplanet_timelapse_maker/application/pixelplanet_timelapse_maker/launcher.exe"

with winshell.shortcut(shortcut_path) as shortcut:
    shortcut.path = target_path
    shortcut.description = "shortcut for ptm"  
    shortcut.icon_location = (target_path, 0)

fromm = os.path.join(current_directory, "pixelplanet_timelapse_maker.lnk")  
to = shortcut_path_desktop

shutil.move(fromm, to)


os.system("cls")
print(" Download finished!")
print(" Old data tarnsferted to new version, enter to quit")
input("")